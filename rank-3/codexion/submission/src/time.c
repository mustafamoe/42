/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   time.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../include/codexion.h"

long long	now_ms(void)
{
	struct timeval	time;

	gettimeofday(&time, NULL);
	return ((long long)time.tv_sec * 1000 + time.tv_usec / 1000);
}

void	make_timespec(long long deadline, struct timespec *time)
{
	time->tv_sec = deadline / 1000;
	time->tv_nsec = (deadline % 1000) * 1000000;
}

void	wait_changed(t_sim *sim, long long deadline)
{
	struct timespec	time;
	long long		remaining;

	remaining = deadline - now_ms();
	if (remaining <= 0)
		return ;
	if (remaining > 10)
	{
		make_timespec(deadline - 10, &time);
		pthread_cond_timedwait(&sim->changed, &sim->state_lock, &time);
	}
	else
	{
		pthread_mutex_unlock(&sim->state_lock);
		usleep(500);
		pthread_mutex_lock(&sim->state_lock);
	}
}

int	wait_until(t_sim *sim, long long deadline)
{
	pthread_mutex_lock(&sim->state_lock);
	while (!sim->stopped && now_ms() < deadline)
		wait_changed(sim, deadline);
	if (sim->stopped)
	{
		pthread_mutex_unlock(&sim->state_lock);
		return (0);
	}
	pthread_mutex_unlock(&sim->state_lock);
	return (1);
}

void	stop_workers(t_sim *sim)
{
	pthread_mutex_lock(&sim->output_lock);
	sim->stopped = 1;
	pthread_cond_signal(&sim->life_changed);
	pthread_cond_broadcast(&sim->print_ready);
	pthread_mutex_unlock(&sim->output_lock);
	pthread_cond_broadcast(&sim->changed);
}
