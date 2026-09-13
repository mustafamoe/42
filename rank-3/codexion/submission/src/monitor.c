/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	find_dead_coder(t_sim *sim, long long now)
{
	int	i;

	i = 0;
	while (i < sim->config.coders)
	{
		if (!sim->coders[i].done && now >= sim->coders[i].last_compile
			+ sim->config.burnout)
			return (sim->coders[i].id);
		i++;
	}
	return (0);
}

static long long	first_deadline(t_sim *sim)
{
	long long	deadline;
	long long	candidate;
	int			i;

	deadline = LLONG_MAX;
	i = 0;
	while (i < sim->config.coders)
	{
		candidate = sim->coders[i].last_compile + sim->config.burnout;
		if (!sim->coders[i].done && candidate < deadline)
			deadline = candidate;
		i++;
	}
	return (deadline);
}

static void	arm_monitor(t_sim *sim)
{
	int	i;
	int	grant_sent;

	sim->monitor_ready = 1;
	pthread_cond_broadcast(&sim->changed);
	while (!sim->started && !sim->stopped)
		pthread_cond_wait(&sim->changed, &sim->state_lock);
	sim->monitor_armed = 1;
	i = 0;
	grant_sent = 0;
	while (i < sim->config.coders)
	{
		if (sim->coders[i].activated && (!sim->coders[i].granted
				|| !grant_sent))
		{
			pthread_cond_signal(&sim->coders[i].ready);
			if (sim->coders[i].granted)
				grant_sent = 1;
		}
		i++;
	}
}

static void	burn_out(t_sim *sim, int id)
{
	sim->death_pending = 1;
	while (sim->printing)
		pthread_cond_wait(&sim->life_changed, &sim->output_lock);
	sim->printing = 1;
	pthread_mutex_unlock(&sim->output_lock);
	log_death(sim, id);
	pthread_mutex_lock(&sim->output_lock);
	sim->printing = 0;
	pthread_cond_broadcast(&sim->print_ready);
	pthread_mutex_unlock(&sim->output_lock);
	pthread_mutex_lock(&sim->state_lock);
	pthread_mutex_lock(&sim->output_lock);
	sim->stopped = 1;
	pthread_cond_signal(&sim->life_changed);
	pthread_mutex_unlock(&sim->output_lock);
	wake_workers(sim);
	pthread_mutex_unlock(&sim->state_lock);
}

void	*monitor_thread(void *data)
{
	t_sim			*sim;
	struct timespec	time;
	long long		deadline;
	int				dead;

	sim = (t_sim *)data;
	pthread_mutex_lock(&sim->state_lock);
	arm_monitor(sim);
	pthread_mutex_lock(&sim->output_lock);
	pthread_mutex_unlock(&sim->state_lock);
	while (!sim->stopped)
	{
		dead = find_dead_coder(sim, now_ms());
		if (dead)
		{
			burn_out(sim, dead);
			return (NULL);
		}
		deadline = first_deadline(sim);
		make_timespec(deadline, &time);
		pthread_cond_timedwait(&sim->life_changed, &sim->output_lock, &time);
	}
	pthread_mutex_unlock(&sim->output_lock);
	return (NULL);
}
