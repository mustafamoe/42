/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_big.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	max_position(t_stack *b)
{
	t_node	*node;
	int		max;
	int		pos;
	int		max_pos;

	node = b->top;
	max = node->index;
	pos = 0;
	max_pos = 0;
	while (node)
	{
		if (node->index > max)
		{
			max = node->index;
			max_pos = pos;
		}
		pos++;
		node = node->next;
	}
	return (max_pos);
}

static void	move_biggest_to_a(t_stack *a, t_stack *b)
{
	int	pos;

	while (b->size > 0)
	{
		pos = max_position(b);
		while (pos > 0 && pos <= b->size / 2)
		{
			rb(b);
			pos--;
		}
		while (pos > b->size / 2)
		{
			rrb(b);
			pos++;
			if (pos == b->size)
				pos = 0;
		}
		pa(a, b);
	}
}

void	chunk_sort(t_stack *a, t_stack *b)
{
	int	pushed;
	int	chunk;

	pushed = 0;
	if (a->size <= 100)
		chunk = 16;
	else
		chunk = 35;
	while (a->size > 0)
	{
		if (a->top->index <= pushed)
		{
			pb(a, b);
			rb(b);
			pushed++;
		}
		else if (a->top->index <= pushed + chunk)
		{
			pb(a, b);
			pushed++;
		}
		else
			ra(a);
	}
	move_biggest_to_a(a, b);
}
