/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   request.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	requests_overlap(t_coder *a, t_coder *b)
{
	return (a->left == b->left || a->left == b->right
		|| a->right == b->left || a->right == b->right);
}

static void	add_request(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	pthread_mutex_lock(&sim->output_lock);
	coder->deadline = coder->last_compile + sim->config.burnout;
	pthread_mutex_unlock(&sim->output_lock);
	coder->sequence = sim->next_sequence++;
	coder->requesting = 1;
	coder->bypassed = 0;
	heap_push(&sim->dongles[coder->left].queue, coder, sim->config.policy);
	if (coder->left != coder->right)
		heap_push(&sim->dongles[coder->right].queue, coder,
			sim->config.policy);
}

static long long	next_schedule_time(t_sim *sim)
{
	long long	deadline;
	long long	now;
	int			i;

	deadline = LLONG_MAX;
	now = now_ms();
	i = 0;
	while (i < sim->config.coders)
	{
		pthread_mutex_lock(&sim->dongles[i].lock);
		if (!sim->dongles[i].held && sim->dongles[i].ready_at > now
			&& sim->dongles[i].ready_at < deadline)
			deadline = sim->dongles[i].ready_at;
		pthread_mutex_unlock(&sim->dongles[i].lock);
		i++;
	}
	return (deadline);
}

static void	wait_for_schedule(t_coder *coder)
{
	struct timespec	time;
	long long		deadline;
	t_sim			*sim;

	sim = coder->sim;
	deadline = next_schedule_time(sim);
	if (deadline == LLONG_MAX)
		pthread_cond_wait(&coder->ready, &sim->state_lock);
	else
	{
		make_timespec(deadline, &time);
		pthread_cond_timedwait(&coder->ready, &sim->state_lock, &time);
	}
	schedule_requests(sim);
}

int	request_dongles(t_coder *coder)
{
	t_sim	*sim;
	int		granted;

	sim = coder->sim;
	pthread_mutex_lock(&sim->state_lock);
	if (sim->stopped)
		return (pthread_mutex_unlock(&sim->state_lock), 0);
	if (!coder->requesting && !coder->granted)
		add_request(coder);
	schedule_requests(sim);
	while (!sim->stopped && !coder->granted)
		wait_for_schedule(coder);
	granted = coder->granted && !sim->stopped;
	coder->granted = 0;
	pthread_mutex_unlock(&sim->state_lock);
	return (granted);
}
