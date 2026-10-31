CC = cc
CFLAGS = -O2 -std=c11 -Wall -Wextra
LDLIBS = -lflint -lgmp -lmpfr
all: verify
verify: verify.c exact.h
	$(CC) $(CFLAGS) -o $@ verify.c $(LDLIBS)
clean:
	rm -f verify
.PHONY: all clean
