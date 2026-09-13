/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <limits.h>
# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/time.h>
# include <time.h>
# include <unistd.h>

typedef enum e_policy
{
	FIFO,
	EDF
}	t_policy;

typedef struct s_config
{
	int			coders;
	long long	burnout;
	long long	compile;
	long long	debug;
	long long	refactor;
	int			goal;
	long long	cooldown;
	t_policy	policy;
}	t_config;

typedef struct s_sim	t_sim;
typedef struct s_coder	t_coder;
typedef pthread_cond_t	t_cond;

typedef struct s_heap
{
	t_coder	**data;
	int		size;
}	t_heap;

typedef struct s_dongle
{
	pthread_mutex_t	lock;
	int				held;
	long long		ready_at;
	t_heap			queue;
}	t_dongle;

struct s_coder
{
	int			id;
	int			left;
	int			right;
	int			compiles;
	int			done;
	int			requesting;
	int			granted;
	int			activated;
	int			bypassed;
	long long	last_compile;
	long long	deadline;
	long long	sequence;
	pthread_t	thread;
	t_cond		ready;
	t_sim		*sim;
};

struct s_sim
{
	t_config		config;
	t_coder			*coders;
	t_dongle		*dongles;
	pthread_mutex_t	state_lock;
	pthread_mutex_t	output_lock;
	pthread_cond_t	changed;
	pthread_cond_t	life_changed;
	pthread_cond_t	print_ready;
	pthread_t		monitor;
	long long		start;
	long long		next_sequence;
	int				started;
	int				stopped;
	int				death_pending;
	int				printing;
	int				completed;
	int				threads_created;
	int				workers_ready;
	int				monitor_created;
	int				monitor_ready;
	int				monitor_armed;
	int				state_ready;
	int				output_ready;
	int				cond_ready;
	int				life_cond_ready;
	int				print_cond_ready;
	int				dongles_ready;
	int				coder_conds_ready;
};

int			parse_args(int argc, char **argv, t_config *config);
int			init_sim(t_sim *sim, t_config *config);
void		cleanup_sim(t_sim *sim);
int			run_simulation(t_sim *sim);
long long	now_ms(void);
void		make_timespec(long long deadline, struct timespec *time);
int			wait_until(t_sim *sim, long long deadline);
void		wake_workers(t_sim *sim);
void		stop_workers(t_sim *sim);
void		heap_push(t_heap *heap, t_coder *coder, t_policy policy);
t_coder		*heap_peek(t_heap *heap);
void		heap_remove(t_heap *heap, t_coder *coder, t_policy policy);
int			request_before(t_coder *a, t_coder *b, t_policy policy);
int			requests_overlap(t_coder *a, t_coder *b);
void		schedule_requests(t_sim *sim);
int			request_dongles(t_coder *coder);
void		pair_mutex(t_coder *coder, int lock);
int			pair_ready(t_coder *coder, long long now);
void		release_dongles(t_coder *coder);
int			log_event(t_sim *sim, int id, char *event);
int			log_compile(t_coder *coder);
void		log_death(t_sim *sim, int id);
void		*coder_thread(void *data);
void		*monitor_thread(void *data);

#endif
