CC = cc
CFLAGS = -O2 -std=c11 -Wall -Wextra
LDLIBS = -lflint -lgmp -lmpfr
all: verifier runner
verifier: verifier.c
runner: runner.c
	$(CC) $(CFLAGS) -o $@ $<
.PHONY: all
