/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_remove.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 16:30:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 16:30:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	swap_coders(t_coder **a, t_coder **b)
{
	t_coder	*swap;

	swap = *a;
	*a = *b;
	*b = swap;
}

static int	move_up(t_heap *heap, int index, t_policy policy)
{
	int	parent;

	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!request_before(heap->data[index], heap->data[parent], policy))
			break ;
		swap_coders(&heap->data[index], &heap->data[parent]);
		index = parent;
	}
	return (index);
}

static void	move_down(t_heap *heap, int index, t_policy policy)
{
	int	child;

	while (index * 2 + 1 < heap->size)
	{
		child = index * 2 + 1;
		if (child + 1 < heap->size && request_before(heap->data[child + 1],
				heap->data[child], policy))
			child++;
		if (!request_before(heap->data[child], heap->data[index], policy))
			break ;
		swap_coders(&heap->data[index], &heap->data[child]);
		index = child;
	}
}

void	heap_remove(t_heap *heap, t_coder *coder, t_policy policy)
{
	int	index;

	index = 0;
	while (index < heap->size && heap->data[index] != coder)
		index++;
	if (index == heap->size)
		return ;
	heap->size--;
	if (index == heap->size)
		return ;
	heap->data[index] = heap->data[heap->size];
	index = move_up(heap, index, policy);
	move_down(heap, index, policy);
}
