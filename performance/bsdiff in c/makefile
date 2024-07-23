# Compiler
CC = gcc

# Compiler Flags
CFLAGS = -std=c99 -Wall -Iinclude

# Source Files
SRCS = src/main.c src/bsdiff.c src/bspatch.c

# Object Files
OBJS = $(SRCS:.c=.o)

# Executable Name
TARGET = build/myprogram

# Default Target
all: $(TARGET)

# Build the executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Compile source files to object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -f src/*.o $(TARGET)

# Phony targets (targets that are not actual files)
.PHONY: all clean
