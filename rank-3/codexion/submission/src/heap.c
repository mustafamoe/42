/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	request_before(t_coder *a, t_coder *b, t_policy policy)
{
	if (policy == FIFO && a->sequence != b->sequence)
		return (a->sequence < b->sequence);
	if (policy == EDF && a->deadline != b->deadline)
		return (a->deadline < b->deadline);
	if (a->sequence != b->sequence)
		return (a->sequence < b->sequence);
	return (a->id < b->id);
}

static void	swap_coders(t_coder **a, t_coder **b)
{
	t_coder	*swap;

	swap = *a;
	*a = *b;
	*b = swap;
}

void	heap_push(t_heap *heap, t_coder *coder, t_policy policy)
{
	int	index;
	int	parent;

	index = heap->size;
	heap->data[index] = coder;
	heap->size++;
	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!request_before(heap->data[index], heap->data[parent], policy))
			break ;
		swap_coders(&heap->data[index], &heap->data[parent]);
		index = parent;
	}
}

t_coder	*heap_peek(t_heap *heap)
{
	if (heap->size == 0)
		return (NULL);
	return (heap->data[0]);
}
