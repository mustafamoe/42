/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_small.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	last_index(t_stack *a)
{
	t_node	*node;

	node = a->top;
	while (node->next)
		node = node->next;
	return (node->index);
}

void	sort_three(t_stack *a)
{
	int	first;
	int	second;
	int	last;

	if (is_sorted(a))
		return ;
	first = a->top->index;
	second = a->top->next->index;
	last = last_index(a);
	if (first > second && first > last)
		ra(a);
	else if (second > first && second > last)
		rra(a);
	if (a->top->index > a->top->next->index)
		sa(a);
}

static int	min_position(t_stack *a)
{
	t_node	*node;
	int		min;
	int		pos;
	int		min_pos;

	node = a->top;
	min = node->index;
	pos = 0;
	min_pos = 0;
	while (node)
	{
		if (node->index < min)
		{
			min = node->index;
			min_pos = pos;
		}
		pos++;
		node = node->next;
	}
	return (min_pos);
}

void	sort_five(t_stack *a, t_stack *b)
{
	int	pos;

	while (a->size > 3)
	{
		pos = min_position(a);
		while (pos > 0 && pos <= a->size / 2)
		{
			ra(a);
			pos--;
		}
		while (pos > a->size / 2)
		{
			rra(a);
			pos++;
			if (pos == a->size)
				pos = 0;
		}
		pb(a, b);
	}
	sort_three(a);
	while (b->size > 0)
		pa(a, b);
}
