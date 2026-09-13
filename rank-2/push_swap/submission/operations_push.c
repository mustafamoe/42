/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   operations_push.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	push(t_stack *dest, t_stack *src)
{
	t_node	*node;

	if (src->size == 0)
		return ;
	node = src->top;
	src->top = src->top->next;
	src->size--;
	node->next = dest->top;
	dest->top = node;
	dest->size++;
}

void	pa(t_stack *a, t_stack *b)
{
	push(a, b);
	write(1, "pa\n", 3);
}

void	pb(t_stack *a, t_stack *b)
{
	push(b, a);
	write(1, "pb\n", 3);
}
