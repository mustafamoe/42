/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	begin_log(t_sim *sim, t_coder *coder, long long *timestamp)
{
	pthread_mutex_lock(&sim->output_lock);
	while (sim->printing && !sim->stopped && !sim->death_pending)
		pthread_cond_wait(&sim->print_ready, &sim->output_lock);
	*timestamp = now_ms();
	if (!simulation_active(sim, *timestamp))
	{
		pthread_mutex_unlock(&sim->output_lock);
		return (0);
	}
	if (coder)
	{
		coder->last_compile = *timestamp;
		pthread_cond_signal(&sim->life_changed);
	}
	sim->printing = 1;
	pthread_mutex_unlock(&sim->output_lock);
	return (1);
}

static void	end_log(t_sim *sim)
{
	pthread_mutex_lock(&sim->output_lock);
	sim->printing = 0;
	if (sim->death_pending)
		pthread_cond_signal(&sim->life_changed);
	else
		pthread_cond_signal(&sim->print_ready);
	pthread_mutex_unlock(&sim->output_lock);
}

int	log_event(t_sim *sim, int id, char *event)
{
	long long	timestamp;

	if (!begin_log(sim, NULL, &timestamp))
		return (0);
	printf("%lld %d %s\n", timestamp - sim->start, id, event);
	end_log(sim);
	return (1);
}

int	log_compile(t_coder *coder)
{
	t_sim		*sim;
	long long	timestamp;

	sim = coder->sim;
	if (!begin_log(sim, coder, &timestamp))
		return (0);
	timestamp -= sim->start;
	printf("%lld %d has taken a dongle\n", timestamp, coder->id);
	printf("%lld %d has taken a dongle\n", timestamp, coder->id);
	printf("%lld %d is compiling\n", timestamp, coder->id);
	end_log(sim);
	return (1);
}

void	log_death(t_sim *sim, int id)
{
	long long	timestamp;

	timestamp = now_ms() - sim->start;
	printf("%lld %d burned out\n", timestamp, id);
}
