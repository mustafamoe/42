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
	if (policy == EDF && a->deadline != b->deadline)
		return (a->deadline < b->deadline);
	if (a->sequence != b->sequence)
		return (a->sequence < b->sequence);
	return (a->id < b->id);
}

void	heap_push(t_heap *heap, t_coder *coder, t_policy policy)
{
	int	index;
	int	parent;

	index = heap->size++;
	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!request_before(coder, heap->data[parent], policy))
			break ;
		heap->data[index] = heap->data[parent];
		index = parent;
	}
	heap->data[index] = coder;
}

t_coder	*heap_peek(t_heap *heap)
{
	if (heap->size == 0)
		return (NULL);
	return (heap->data[0]);
}

void	heap_pop(t_heap *heap)
{
	if (heap->size > 0)
	{
		heap->size--;
		heap->data[0] = heap->data[heap->size];
	}
}
