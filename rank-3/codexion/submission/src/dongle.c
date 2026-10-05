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

#include "../include/codexion.h"

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

int	pair_ready(t_coder *coder, long long *retry_at)
{
	t_dongle	*left;
	t_dongle	*right;
	int			ready;

	left = &coder->sim->dongles[coder->left];
	right = &coder->sim->dongles[coder->right];
	pair_mutex(coder, 1);
	ready = !left->held && !right->held;
	if (ready)
	{
		*retry_at = left->ready_at;
		if (right->ready_at > *retry_at)
			*retry_at = right->ready_at;
		ready = *retry_at <= now_ms();
	}
	pair_mutex(coder, 0);
	return (ready);
}

void	release_dongles(t_coder *coder)
{
	t_sim		*sim;
	t_dongle	*left;
	t_dongle	*right;

	sim = coder->sim;
	left = &sim->dongles[coder->left];
	right = &sim->dongles[coder->right];
	pthread_mutex_lock(&sim->state_lock);
	pair_mutex(coder, 1);
	left->ready_at = now_ms() + sim->config.cooldown;
	right->ready_at = left->ready_at;
	left->held = 0;
	right->held = 0;
	pair_mutex(coder, 0);
	pthread_cond_broadcast(&sim->changed);
	pthread_mutex_unlock(&sim->state_lock);
}
