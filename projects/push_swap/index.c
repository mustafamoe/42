/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   index.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	has_duplicate(t_stack *stack)
{
	t_node	*a;
	t_node	*b;

	a = stack->top;
	while (a)
	{
		b = a->next;
		while (b)
		{
			if (a->value == b->value)
				return (1);
			b = b->next;
		}
		a = a->next;
	}
	return (0);
}

void	set_indexes(t_stack *stack)
{
	t_node	*a;
	t_node	*b;
	int		index;

	a = stack->top;
	while (a)
	{
		index = 0;
		b = stack->top;
		while (b)
		{
			if (b->value < a->value)
				index++;
			b = b->next;
		}
		a->index = index;
		a = a->next;
	}
}
