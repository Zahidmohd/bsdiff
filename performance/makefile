CC = gcc
CFLAGS = -std=c99 -Wall -I"C:/msys64/mingw64/include"
LDFLAGS = -L"C:/msys64/mingw64/lib" -lbz2
TARGET = test

all: $(TARGET)

$(TARGET): test.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

test.o: test.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f test.o $(TARGET)

.PHONY: all clean
