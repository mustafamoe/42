/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mustafamoe <mustafamoe@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/17 18:10:00 by mustafamoe        #+#    #+#             */
/*   Updated: 2026/05/17 18:10:00 by mustafamoe       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	parse_number(char *s, int *i, int *out)
{
	long	num;
	int		sign;

	num = 0;
	sign = 1;
	if (s[*i] == '+' || s[*i] == '-')
	{
		if (s[*i] == '-')
			sign = -1;
		(*i)++;
	}
	if (!is_digit(s[*i]))
		return (0);
	while (is_digit(s[*i]))
	{
		num = num * 10 + (s[*i] - '0');
		if ((sign == 1 && num > INT_MAX)
			|| (sign == -1 && num > 2147483648L))
			return (0);
		(*i)++;
	}
	*out = (int)(num * sign);
	return (1);
}

static int	parse_one_arg(char *s, t_stack *a)
{
	t_node	*node;
	int		i;
	int		value;
	int		found;

	i = 0;
	found = 0;
	while (s[i])
	{
		while (is_space(s[i]))
			i++;
		if (!s[i])
			break ;
		if (!parse_number(s, &i, &value))
			return (0);
		if (s[i] && !is_space(s[i]))
			return (0);
		node = new_node(value);
		if (!node)
			return (0);
		add_back(a, node);
		a->size++;
		found = 1;
	}
	return (found);
}

int	parse_args(int argc, char **argv, t_stack *a)
{
	int	i;

	i = 1;
	while (i < argc)
	{
		if (!parse_one_arg(argv[i], a))
			return (0);
		i++;
	}
	return (1);
}
