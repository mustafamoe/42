/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*new_node(int value)
{
	t_node	*node;

	node = malloc(sizeof(t_node));
	if (!node)
		return (NULL);
	node->value = value;
	node->index = 0;
	node->next = NULL;
	return (node);
}

void	add_back(t_stack *stack, t_node *node)
{
	t_node	*tmp;

	if (!stack->top)
	{
		stack->top = node;
		return ;
	}
	tmp = stack->top;
	while (tmp->next)
		tmp = tmp->next;
	tmp->next = node;
}

void	free_stack(t_stack *stack)
{
	t_node	*tmp;

	while (stack->top)
	{
		tmp = stack->top->next;
		free(stack->top);
		stack->top = tmp;
	}
	stack->size = 0;
}
