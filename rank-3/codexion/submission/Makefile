NAME := codexion
CC := cc
CFLAGS := -Wall -Wextra -Werror -pthread
CPPFLAGS := -Iinclude

SRCS := src/main.c src/parse.c src/init.c src/time.c src/heap.c \
	src/request.c src/log.c src/coder.c \
	src/dongle.c src/monitor.c src/run.c
OBJS := $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

src/%.o: src/%.c include/codexion.h
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
