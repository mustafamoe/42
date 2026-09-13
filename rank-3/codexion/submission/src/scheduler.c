/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 16:30:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 16:30:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_coder	*best_pending(t_sim *sim)
{
	t_coder	*best;
	t_coder	*coder;
	int		i;

	best = NULL;
	i = 0;
	while (i < sim->config.coders)
	{
		coder = heap_peek(&sim->dongles[i].queue);
		if (coder && (!best
				|| request_before(coder, best, sim->config.policy)))
			best = coder;
		i++;
	}
	return (best);
}

static t_coder	*best_eligible(t_sim *sim, t_coder *protect, long long now)
{
	t_coder	*best;
	t_coder	*coder;
	int		i;
	int		index;

	best = NULL;
	i = 0;
	while (i < sim->config.coders)
	{
		index = 0;
		while (index < sim->dongles[i].queue.size)
		{
			coder = sim->dongles[i].queue.data[index];
			if ((!protect || !requests_overlap(coder, protect))
				&& pair_ready(coder, now) && (!best
					|| request_before(coder, best, sim->config.policy)))
				best = coder;
			index++;
		}
		i++;
	}
	return (best);
}

static void	grant_request(t_sim *sim, t_coder *coder)
{
	t_dongle	*left;
	t_dongle	*right;

	left = &sim->dongles[coder->left];
	right = &sim->dongles[coder->right];
	pair_mutex(coder, 1);
	heap_remove(&left->queue, coder, sim->config.policy);
	if (left != right)
		heap_remove(&right->queue, coder, sim->config.policy);
	left->held = 1;
	right->held = 1;
	coder->requesting = 0;
	coder->granted = 1;
	coder->activated = 1;
	pthread_cond_signal(&coder->ready);
	pair_mutex(coder, 0);
}

static t_coder	*next_candidate(t_sim *sim, t_coder *priority, long long now)
{
	t_coder	*candidate;

	if (priority->bypassed)
		return (best_eligible(sim, priority, now));
	candidate = best_eligible(sim, NULL, now);
	if (!candidate || !requests_overlap(candidate, priority))
		return (candidate);
	if (sim->config.policy == EDF && now + sim->config.compile
		+ sim->config.cooldown + 10 >= priority->deadline)
	{
		priority->bypassed = 1;
		return (best_eligible(sim, priority, now));
	}
	priority->bypassed = 1;
	return (candidate);
}

void	schedule_requests(t_sim *sim)
{
	t_coder		*priority;
	t_coder		*candidate;
	long long	now;

	now = now_ms();
	priority = best_pending(sim);
	while (priority && pair_ready(priority, now))
	{
		grant_request(sim, priority);
		priority = best_pending(sim);
	}
	candidate = NULL;
	if (priority && now < priority->deadline)
		candidate = next_candidate(sim, priority, now);
	while (candidate)
	{
		grant_request(sim, candidate);
		candidate = next_candidate(sim, priority, now);
	}
	if (priority)
	{
		priority->activated = 1;
		pthread_cond_signal(&priority->ready);
	}
}
