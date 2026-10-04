#include "codexion.h"
#include <assert.h>
#include <errno.h>

/* Private fault injection; no test hooks or globals enter submission/. */
static long long test_time = 1000;
static t_sim *delayed_sim;
static int allocation_failure;
static int mutex_failure;
static int condition_failure;
static int creation_failure;

long long now_ms(void)
{
    return test_time;
}

#define now_ms real_now_ms
#include "../submission/src/time.c"
#undef now_ms

static int delayed_lock(pthread_mutex_t *lock)
{
    if (delayed_sim && lock == &delayed_sim->state_lock)
        test_time += 100;
    return pthread_mutex_lock(lock);
}

#define pthread_mutex_lock delayed_lock
#include "../submission/src/dongle.c"
#undef pthread_mutex_lock

static void *test_malloc(size_t size)
{
    if (allocation_failure && --allocation_failure == 0)
        return NULL;
    return malloc(size);
}

static int test_mutex_init(pthread_mutex_t *lock,
    const pthread_mutexattr_t *attributes)
{
    if (mutex_failure && --mutex_failure == 0)
        return EAGAIN;
    return pthread_mutex_init(lock, attributes);
}

static int test_cond_init(pthread_cond_t *condition,
    const pthread_condattr_t *attributes)
{
    if (condition_failure && --condition_failure == 0)
        return EAGAIN;
    return pthread_cond_init(condition, attributes);
}

#define malloc test_malloc
#define pthread_mutex_init test_mutex_init
#define pthread_cond_init test_cond_init
#include "../submission/src/init.c"
#undef malloc
#undef pthread_mutex_init
#undef pthread_cond_init

static int test_create(pthread_t *thread, const pthread_attr_t *attributes,
    void *(*start)(void *), void *data)
{
    if (creation_failure && --creation_failure == 0)
        return EAGAIN;
    return pthread_create(thread, attributes, start, data);
}

#define pthread_create test_create
#include "../submission/src/run.c"
#undef pthread_create
#include "../submission/src/request.c"
#include "../submission/src/coder.c"

static void setup(t_sim *sim, t_policy policy)
{
    t_config config = {4, 1000, 50, 10, 10, 1, 20, policy};

    assert(init_sim(sim, &config));
    sim->start = test_time;
    for (int i = 0; i < config.coders; i++)
        sim->coders[i].last_compile = test_time;
}

static void ordering(t_policy policy)
{
    t_sim sim;
    long long retry;

    setup(&sim, policy);
    pthread_mutex_lock(&sim.state_lock);
    for (int i = 0; i < 4; i++)
    {
        /* Different deadlines make EDF ordering independent of tie rules. */
        sim.coders[i].last_compile -= 40 - i * 10;
        queue_request(&sim.coders[i]);
    }
    assert(take_dongles(&sim.coders[0], &retry));
    assert(!take_dongles(&sim.coders[2], &retry));
    assert(heap_peek(&sim.dongles[2].queue) == &sim.coders[1]);
    pthread_mutex_unlock(&sim.state_lock);
    release_dongles(&sim.coders[0]);
    test_time += sim.config.cooldown;
    pthread_mutex_lock(&sim.state_lock);
    assert(take_dongles(&sim.coders[1], &retry));
    pthread_mutex_unlock(&sim.state_lock);
    cleanup_sim(&sim);
}

static void heap_and_parallel_grants(void)
{
    t_sim sim;
    long long retry;
    t_heap heap = {{NULL, NULL}, 0};

    setup(&sim, EDF);
    sim.coders[0].deadline = test_time + 100;
    sim.coders[1].deadline = test_time + 200;
    sim.coders[0].sequence = 2;
    sim.coders[1].sequence = 1;
    assert(request_before(&sim.coders[1], &sim.coders[0], FIFO));
    heap_push(&heap, &sim.coders[1], EDF);
    heap_push(&heap, &sim.coders[0], EDF);
    assert(heap_peek(&heap) == &sim.coders[0]);
    heap_pop(&heap);
    assert(heap_peek(&heap) == &sim.coders[1]);
    heap_pop(&heap);
    assert(heap_peek(&heap) == NULL);
    sim.coders[0].deadline = sim.coders[1].deadline;
    assert(request_before(&sim.coders[1], &sim.coders[0], EDF));
    sim.coders[0].sequence = sim.coders[1].sequence;
    assert(request_before(&sim.coders[0], &sim.coders[1], EDF));
    pthread_mutex_lock(&sim.state_lock);
    queue_initial_requests(&sim);
    assert(take_dongles(&sim.coders[0], &retry));
    assert(take_dongles(&sim.coders[2], &retry));
    pthread_mutex_unlock(&sim.state_lock);
    cleanup_sim(&sim);
}

static void cooldown_after_lock(void)
{
    t_sim sim;
    long long retry = 0;

    setup(&sim, FIFO);
    sim.dongles[0].held = 1;
    sim.dongles[1].held = 1;
    delayed_sim = &sim;
    release_dongles(&sim.coders[0]);
    delayed_sim = NULL;
    assert(sim.dongles[0].ready_at == test_time + 20);
    assert(sim.dongles[1].ready_at == test_time + 20);
    pthread_mutex_lock(&sim.state_lock);
    queue_request(&sim.coders[0]);
    assert(!take_dongles(&sim.coders[0], &retry));
    assert(retry == test_time + 20);
    test_time += 20;
    assert(take_dongles(&sim.coders[0], &retry));
    pthread_mutex_unlock(&sim.state_lock);
    cleanup_sim(&sim);
}

static void expired_transitions(void)
{
    t_sim sim;
    long long previous;

    setup(&sim, EDF);
    sim.coders[0].last_compile = test_time - sim.config.burnout;
    previous = sim.coders[0].last_compile;
    assert(!log_compile(&sim.coders[0]));
    assert(sim.coders[0].last_compile == previous);
    assert(sim.death_pending == 1);
    cleanup_sim(&sim);
    setup(&sim, EDF);
    sim.coders[0].last_compile = test_time - sim.config.burnout;
    assert(finish_compile(&sim.coders[0]));
    assert(sim.coders[0].compiles == 0 && sim.completed == 0);
    assert(sim.death_pending == 1 && !sim.stopped);
    cleanup_sim(&sim);
    setup(&sim, EDF);
    sim.coders[0].last_compile = test_time - sim.config.burnout;
    assert(!log_compile(&sim.coders[1]));
    assert(sim.death_pending == 1);
    cleanup_sim(&sim);
}

static void global_completion(void)
{
    t_sim sim;

    setup(&sim, FIFO);
    assert(!finish_compile(&sim.coders[0]));
    assert(!finish_compile(&sim.coders[0]));
    assert(sim.completed == 1 && sim.coders[0].compiles == 1);
    for (int i = 1; i < 3; i++)
        assert(!finish_compile(&sim.coders[i]));
    assert(finish_compile(&sim.coders[3]));
    assert(sim.stopped && sim.completed == 4 && !sim.death_pending);
    cleanup_sim(&sim);
    setup(&sim, FIFO);
    assert(!finish_compile(&sim.coders[0]));
    test_time += sim.config.burnout;
    pthread_mutex_lock(&sim.output_lock);
    assert(!simulation_active(&sim, test_time));
    assert(sim.death_pending == 1);
    pthread_mutex_unlock(&sim.output_lock);
    cleanup_sim(&sim);
}

static void partial_failures(void)
{
    t_config config = {4, 1000, 50, 10, 10, 1, 20, FIFO};
    t_sim sim;

    for (int i = 1; i <= 2; i++)
    {
        allocation_failure = i;
        assert(!init_sim(&sim, &config));
    }
    for (int i = 1; i <= 6; i++)
    {
        mutex_failure = i;
        assert(!init_sim(&sim, &config));
    }
    for (int i = 1; i <= 3; i++)
    {
        condition_failure = i;
        assert(!init_sim(&sim, &config));
    }
    for (int i = 1; i <= 5; i++)
    {
        setup(&sim, FIFO);
        creation_failure = i;
        assert(!run_simulation(&sim));
        assert(sim.stopped && sim.threads_created == i - 1);
        cleanup_sim(&sim);
    }
}

int main(void)
{
    ordering(FIFO);
    ordering(EDF);
    heap_and_parallel_grants();
    cooldown_after_lock();
    expired_transitions();
    global_completion();
    partial_failures();
    puts("Codexion regression checks passed");
    return 0;
}
