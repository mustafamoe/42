/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_number(char *text, long long *number)
{
	int			i;
	long long	value;

	if (!text[0])
		return (0);
	i = 0;
	value = 0;
	while (text[i])
	{
		if (text[i] < '0' || text[i] > '9')
			return (0);
		if (value > (INT_MAX - (text[i] - '0')) / 10)
			return (0);
		value = value * 10 + text[i] - '0';
		i++;
	}
	*number = value;
	return (1);
}

static int	parse_policy(char *text, t_policy *policy)
{
	if (strcmp(text, "fifo") == 0)
		*policy = FIFO;
	else if (strcmp(text, "edf") == 0)
		*policy = EDF;
	else
		return (0);
	return (1);
}

int	parse_args(int argc, char **argv, t_config *config)
{
	long long	values[7];
	int			i;

	if (argc != 9)
		return (0);
	i = 0;
	while (i < 7)
	{
		if (!parse_number(argv[i + 1], &values[i]))
			return (0);
		i++;
	}
	config->coders = (int)values[0];
	config->burnout = values[1];
	config->compile = values[2];
	config->debug = values[3];
	config->refactor = values[4];
	config->goal = (int)values[5];
	config->cooldown = values[6];
	if (config->coders == 0 || config->burnout == 0 || config->goal == 0)
		return (0);
	return (parse_policy(argv[8], &config->policy));
}
