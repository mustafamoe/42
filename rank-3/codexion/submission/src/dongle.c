/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 15:15:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 15:15:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	pair_mutex(t_coder *coder, int lock)
{
	t_sim	*sim;
	int		first;
	int		second;

	sim = coder->sim;
	first = coder->left;
	second = coder->right;
	if (first > second)
	{
		first = coder->right;
		second = coder->left;
	}
	if (lock)
		pthread_mutex_lock(&sim->dongles[first].lock);
	else
		pthread_mutex_unlock(&sim->dongles[first].lock);
	if (first != second && lock)
		pthread_mutex_lock(&sim->dongles[second].lock);
	else if (first != second)
		pthread_mutex_unlock(&sim->dongles[second].lock);
}

int	pair_ready(t_coder *coder, long long now)
{
	t_sim		*sim;
	t_dongle	*left;
	t_dongle	*right;
	int			ready;

	if (now >= coder->deadline)
		return (0);
	sim = coder->sim;
	left = &sim->dongles[coder->left];
	right = &sim->dongles[coder->right];
	pair_mutex(coder, 1);
	ready = !left->held && !right->held && left->ready_at <= now
		&& right->ready_at <= now;
	pair_mutex(coder, 0);
	return (ready);
}

static void	free_dongle(t_dongle *dongle, long long ready_at)
{
	pthread_mutex_lock(&dongle->lock);
	dongle->held = 0;
	dongle->ready_at = ready_at;
	pthread_mutex_unlock(&dongle->lock);
}

void	release_dongles(t_coder *coder)
{
	t_sim		*sim;
	long long	ready_at;

	sim = coder->sim;
	ready_at = now_ms() + sim->config.cooldown;
	pthread_mutex_lock(&sim->state_lock);
	free_dongle(&sim->dongles[coder->left], ready_at);
	if (coder->left != coder->right)
		free_dongle(&sim->dongles[coder->right], ready_at);
	schedule_requests(sim);
	pthread_mutex_unlock(&sim->state_lock);
}
