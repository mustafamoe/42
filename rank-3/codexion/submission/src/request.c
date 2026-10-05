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

#include "../include/codexion.h"

void	queue_request(t_coder *coder)
{
	t_sim	*sim;

	sim = coder->sim;
	pthread_mutex_lock(&sim->output_lock);
	coder->deadline = coder->last_compile + sim->config.burnout;
	pthread_mutex_unlock(&sim->output_lock);
	coder->sequence = sim->next_sequence++;
	coder->requesting = 1;
	heap_push(&sim->dongles[coder->left].queue, coder, sim->config.policy);
	if (coder->left != coder->right)
		heap_push(&sim->dongles[coder->right].queue, coder,
			sim->config.policy);
}

static int	take_dongles(t_coder *coder, long long *retry_at)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &coder->sim->dongles[coder->left];
	right = &coder->sim->dongles[coder->right];
	*retry_at = 0;
	if (heap_peek(&left->queue) != coder
		|| heap_peek(&right->queue) != coder
		|| !pair_ready(coder, retry_at))
		return (0);
	pair_mutex(coder, 1);
	heap_pop(&left->queue);
	if (left != right)
		heap_pop(&right->queue);
	left->held = 1;
	right->held = 1;
	coder->requesting = 0;
	pair_mutex(coder, 0);
	return (1);
}

int	request_dongles(t_coder *coder)
{
	t_sim		*sim;
	long long	retry_at;
	int			taken;

	sim = coder->sim;
	pthread_mutex_lock(&sim->state_lock);
	if (sim->stopped)
		return (pthread_mutex_unlock(&sim->state_lock), 0);
	if (!coder->requesting)
		queue_request(coder);
	while (!sim->stopped && !take_dongles(coder, &retry_at))
	{
		if (retry_at)
			wait_changed(sim, retry_at);
		else
			pthread_cond_wait(&sim->changed, &sim->state_lock);
	}
	taken = !sim->stopped;
	pthread_mutex_unlock(&sim->state_lock);
	return (taken);
}
