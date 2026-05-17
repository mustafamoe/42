NAME = push_swap
CC = cc
CFLAGS = -Wall -Wextra -Werror

SRC = main.c parse.c stack.c operations.c operations_push.c \
	operations_rotate.c operations_reverse.c index.c sort.c sort_small.c \
	sort_big.c utils.c
OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
