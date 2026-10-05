/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

static int	record_compile(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	if (coder->compiles < sim->config.goal)
	{
		coder->compiles++;
		if (coder->compiles == sim->config.goal)
			sim->completed++;
	}
	if (sim->completed == sim->config.coders)
		sim->stopped = 1;
	return (sim->stopped);
}

static int	finish_compile(t_coder *coder)
{
	t_sim	*sim;
	int		done;

	sim = coder->sim;
	pthread_mutex_lock(&sim->state_lock);
	pthread_mutex_lock(&sim->output_lock);
	if (!simulation_active(sim, now_ms()))
		done = 1;
	else
		done = record_compile(coder);
	pthread_cond_signal(&sim->life_changed);
	if (sim->stopped)
		pthread_cond_broadcast(&sim->print_ready);
	pthread_mutex_unlock(&sim->output_lock);
	if (sim->stopped)
		pthread_cond_broadcast(&sim->changed);
	pthread_mutex_unlock(&sim->state_lock);
	return (done);
}

static int	use_dongles(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	if (coder->left == coder->right)
	{
		if (!log_event(sim, coder->id, "has taken a dongle"))
			return (0);
		pthread_mutex_lock(&sim->state_lock);
		while (!sim->stopped)
			pthread_cond_wait(&sim->changed, &sim->state_lock);
		pthread_mutex_unlock(&sim->state_lock);
		return (0);
	}
	return (log_compile(coder));
}

static int	compile_cycle(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	if (!request_dongles(coder))
		return (0);
	if (!use_dongles(coder))
		return (release_dongles(coder), 0);
	if (!wait_until(sim, coder->last_compile + sim->config.compile))
		return (release_dongles(coder), 0);
	release_dongles(coder);
	if (finish_compile(coder))
		return (0);
	if (!log_event(sim, coder->id, "is debugging")
		|| !wait_until(sim, now_ms() + sim->config.debug))
		return (0);
	if (!log_event(sim, coder->id, "is refactoring")
		|| !wait_until(sim, now_ms() + sim->config.refactor))
		return (0);
	return (1);
}

void	*coder_thread(void *data)
{
	t_coder	*coder;
	t_sim	*sim;

	coder = (t_coder *)data;
	sim = coder->sim;
	pthread_mutex_lock(&sim->state_lock);
	sim->workers_ready++;
	pthread_cond_broadcast(&sim->changed);
	while ((!sim->started || !sim->monitor_armed)
		&& !sim->stopped)
		pthread_cond_wait(&sim->changed, &sim->state_lock);
	pthread_mutex_unlock(&sim->state_lock);
	if (sim->config.coders > 1 && sim->config.coders % 2)
		wait_until(sim, sim->start + coder->sequence
			* (sim->config.compile + sim->config.cooldown)
			/ (sim->config.coders / 2));
	while (compile_cycle(coder))
		;
	return (NULL);
}
