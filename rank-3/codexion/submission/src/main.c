/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mal-hall <mal-hall@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/08/30 13:45:00 by mal-hall          #+#    #+#             */
/*   Updated: 2026/08/30 13:45:00 by mal-hall         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int argc, char **argv)
{
	t_config	config;
	t_sim		sim;
	int			status;

	if (!parse_args(argc, argv, &config))
		return (write(2, "Error\n", 6), 1);
	if (!init_sim(&sim, &config))
		return (write(2, "Error\n", 6), 1);
	status = run_simulation(&sim);
	cleanup_sim(&sim);
	if (!status)
		return (write(2, "Error\n", 6), 1);
	return (0);
}
