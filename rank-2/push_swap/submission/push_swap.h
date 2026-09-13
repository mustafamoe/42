/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <limits.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_node
{
	int				value;
	int				index;
	struct s_node	*next;
}	t_node;

typedef struct s_stack
{
	t_node	*top;
	int		size;
}	t_stack;

int		parse_args(int argc, char **argv, t_stack *a);
int		has_duplicate(t_stack *stack);
void	set_indexes(t_stack *stack);
void	sort_stack(t_stack *a, t_stack *b);
void	sort_three(t_stack *a);
void	sort_five(t_stack *a, t_stack *b);
void	chunk_sort(t_stack *a, t_stack *b);
void	sa(t_stack *a);
void	pa(t_stack *a, t_stack *b);
void	pb(t_stack *a, t_stack *b);
void	ra(t_stack *a);
void	rb(t_stack *b);
void	rra(t_stack *a);
void	rrb(t_stack *b);
t_node	*new_node(int value);
void	add_back(t_stack *stack, t_node *node);
void	free_stack(t_stack *stack);
int		is_sorted(t_stack *stack);
int		write_error(void);
int		is_space(char c);
int		is_digit(char c);

#endif
