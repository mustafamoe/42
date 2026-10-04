/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   run.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	create_threads(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coders)
	{
		if (pthread_create(&sim->coders[i].thread, NULL,
				coder_thread, &sim->coders[i]) != 0)
			return (0);
		sim->threads_created++;
		i++;
	}
	if (pthread_create(&sim->monitor, NULL, monitor_thread, sim) != 0)
		return (0);
	sim->monitor_created = 1;
	return (1);
}

static void	queue_initial_requests(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coders)
	{
		queue_request(&sim->coders[i]);
		i += 2;
		if (i >= sim->config.coders && i % 2 == 0)
			i = 1;
	}
}

static void	start_threads(t_sim *sim, int failed)
{
	int	i;

	pthread_mutex_lock(&sim->state_lock);
	while (!failed && (!sim->monitor_ready
			|| sim->workers_ready != sim->threads_created))
		pthread_cond_wait(&sim->changed, &sim->state_lock);
	if (!failed)
		queue_initial_requests(sim);
	sim->start = now_ms();
	i = 0;
	while (i < sim->config.coders)
	{
		sim->coders[i].last_compile = sim->start;
		sim->coders[i].deadline = sim->start + sim->config.burnout;
		i++;
	}
	sim->started = 1;
	if (failed)
		stop_workers(sim);
	pthread_cond_broadcast(&sim->changed);
	pthread_mutex_unlock(&sim->state_lock);
}

static void	join_threads(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->threads_created)
	{
		pthread_join(sim->coders[i].thread, NULL);
		i++;
	}
	if (sim->monitor_created)
		pthread_join(sim->monitor, NULL);
}

int	run_simulation(t_sim *sim)
{
	int	created;

	created = create_threads(sim);
	start_threads(sim, !created);
	join_threads(sim);
	return (created);
}
