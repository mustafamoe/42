/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_locks(t_sim *sim)
{
	if (pthread_mutex_init(&sim->state_lock, NULL) != 0)
		return (0);
	sim->state_ready = 1;
	if (pthread_mutex_init(&sim->output_lock, NULL) != 0)
		return (0);
	sim->output_ready = 1;
	if (pthread_cond_init(&sim->changed, NULL) != 0)
		return (0);
	sim->cond_ready = 1;
	if (pthread_cond_init(&sim->life_changed, NULL) != 0)
		return (0);
	sim->life_cond_ready = 1;
	if (pthread_cond_init(&sim->print_ready, NULL) != 0)
		return (0);
	sim->print_cond_ready = 1;
	return (1);
}

static int	init_dongles(t_sim *sim)
{
	int	i;

	sim->dongles = malloc(sizeof(t_dongle) * sim->config.coders);
	if (!sim->dongles)
		return (0);
	memset(sim->dongles, 0, sizeof(t_dongle) * sim->config.coders);
	i = 0;
	while (i < sim->config.coders)
	{
		sim->dongles[i].queue.data = malloc(sizeof(t_coder *) * 2);
		if (!sim->dongles[i].queue.data)
			return (0);
		if (pthread_mutex_init(&sim->dongles[i].lock, NULL) != 0)
			return (0);
		sim->dongles_ready++;
		i++;
	}
	return (1);
}

static int	init_coders(t_sim *sim)
{
	int	i;

	sim->coders = malloc(sizeof(t_coder) * sim->config.coders);
	if (!sim->coders)
		return (0);
	memset(sim->coders, 0, sizeof(t_coder) * sim->config.coders);
	i = 0;
	while (i < sim->config.coders)
	{
		sim->coders[i].id = i + 1;
		sim->coders[i].left = i;
		sim->coders[i].right = (i + 1) % sim->config.coders;
		sim->coders[i].sim = sim;
		if (pthread_cond_init(&sim->coders[i].ready, NULL) != 0)
			return (0);
		sim->coder_conds_ready++;
		i++;
	}
	return (1);
}

void	cleanup_sim(t_sim *sim)
{
	int	i;

	i = 0;
	while (sim->dongles && i < sim->config.coders)
	{
		if (i < sim->dongles_ready)
			pthread_mutex_destroy(&sim->dongles[i].lock);
		free(sim->dongles[i].queue.data);
		i++;
	}
	i = 0;
	while (sim->coders && i < sim->coder_conds_ready)
		pthread_cond_destroy(&sim->coders[i++].ready);
	free(sim->dongles);
	free(sim->coders);
	if (sim->cond_ready)
		pthread_cond_destroy(&sim->changed);
	if (sim->life_cond_ready)
		pthread_cond_destroy(&sim->life_changed);
	if (sim->print_cond_ready)
		pthread_cond_destroy(&sim->print_ready);
	if (sim->output_ready)
		pthread_mutex_destroy(&sim->output_lock);
	if (sim->state_ready)
		pthread_mutex_destroy(&sim->state_lock);
}

int	init_sim(t_sim *sim, t_config *config)
{
	memset(sim, 0, sizeof(*sim));
	sim->config.coders = config->coders;
	sim->config.burnout = config->burnout;
	sim->config.compile = config->compile;
	sim->config.debug = config->debug;
	sim->config.refactor = config->refactor;
	sim->config.goal = config->goal;
	sim->config.cooldown = config->cooldown;
	sim->config.policy = config->policy;
	if (!init_locks(sim) || !init_dongles(sim) || !init_coders(sim))
	{
		cleanup_sim(sim);
		return (0);
	}
	return (1);
}
