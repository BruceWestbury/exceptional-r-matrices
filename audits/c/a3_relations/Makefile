CC = cc
CFLAGS = -O2 -std=c11 -Wall -Wextra
LDLIBS = -lflint -lgmp -lmpfr
all: verify runner
verify: verify.c json_reader.h
	$(CC) $(CFLAGS) -o $@ verify.c $(LDLIBS)
runner: runner.c
	$(CC) $(CFLAGS) -o $@ runner.c
.PHONY: all
