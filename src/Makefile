CC = gcc
CFLAGS = -I./tensorflow-lite/include
LDFLAGS = -L./tensorflow-lite/lib -ltensorflowlite_c -lm

all: client_steering

client_steering: client_steering.c
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

