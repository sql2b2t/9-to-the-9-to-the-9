CC ?= cc
CFLAGS ?= -O2
LDLIBS = -lgmp

all: pow9

pow9: src/pow9.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f pow9

.PHONY: all clean
