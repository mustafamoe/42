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

int	simulation_active(t_sim *sim, long long now)
{
	int	i;

	if (sim->stopped || sim->death_pending)
		return (0);
	i = 0;
	while (i < sim->config.coders)
	{
		if (now >= sim->coders[i].last_compile + sim->config.burnout)
		{
			sim->death_pending = sim->coders[i].id;
			pthread_cond_signal(&sim->life_changed);
			pthread_cond_broadcast(&sim->print_ready);
			return (0);
		}
		i++;
	}
	return (1);
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
		if (candidate < deadline)
			deadline = candidate;
		i++;
	}
	return (deadline);
}

static void	arm_monitor(t_sim *sim)
{
	sim->monitor_ready = 1;
	pthread_cond_broadcast(&sim->changed);
	while (!sim->started && !sim->stopped)
		pthread_cond_wait(&sim->changed, &sim->state_lock);
	sim->monitor_armed = 1;
	pthread_cond_broadcast(&sim->changed);
}

static void	burn_out(t_sim *sim)
{
	while (sim->printing)
		pthread_cond_wait(&sim->life_changed, &sim->output_lock);
	sim->printing = 1;
	pthread_mutex_unlock(&sim->output_lock);
	log_death(sim, sim->death_pending);
	pthread_mutex_lock(&sim->output_lock);
	sim->printing = 0;
	pthread_cond_broadcast(&sim->print_ready);
	pthread_mutex_unlock(&sim->output_lock);
	pthread_mutex_lock(&sim->state_lock);
	pthread_mutex_lock(&sim->output_lock);
	sim->stopped = 1;
	pthread_cond_signal(&sim->life_changed);
	pthread_mutex_unlock(&sim->output_lock);
	pthread_cond_broadcast(&sim->changed);
	pthread_mutex_unlock(&sim->state_lock);
}

void	*monitor_thread(void *data)
{
	t_sim			*sim;
	struct timespec	time;
	long long		deadline;

	sim = (t_sim *)data;
	pthread_mutex_lock(&sim->state_lock);
	arm_monitor(sim);
	pthread_mutex_lock(&sim->output_lock);
	pthread_mutex_unlock(&sim->state_lock);
	while (!sim->stopped)
	{
		if (!simulation_active(sim, now_ms()))
		{
			burn_out(sim);
			return (NULL);
		}
		deadline = first_deadline(sim);
		make_timespec(deadline, &time);
		pthread_cond_timedwait(&sim->life_changed, &sim->output_lock, &time);
	}
	pthread_mutex_unlock(&sim->output_lock);
	return (NULL);
}
