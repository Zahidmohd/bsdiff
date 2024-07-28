# Compiler
CC = gcc

# vcpkg include and library paths (assuming default vcpkg installation path)
VCPKG_INCLUDE_PATH = C:/Users/zahid/OneDrive/Desktop/python/bsdiff4/performance/vcpkg/packages/bzip2_x64-windows/include
VCPKG_LIB_PATH = C:\Users\zahid\OneDrive\Desktop\python\bsdiff4\performance\vcpkg\packages\bzip2_x64-windows\debug\lib

# Compiler Flags
CFLAGS = -std=c99 -Wall -g -Iinclude -I"$(VCPKG_INCLUDE_PATH)"

# Linker Flags
LDFLAGS = -L"C:/Users/zahid/OneDrive/Desktop/python/bsdiff4/performance/vcpkg/packages/bzip2_x64-windows/lib" -lbz2


# Source Files
SRCS = src/main.c src/bsdiff.c src/bspatch.c

# Object Files
OBJS = $(SRCS:.c=.o)

# Output Directory
BUILD_DIR = build

# Executable Name
TARGET = $(BUILD_DIR)/myprogram

# Default Target
all: $(BUILD_DIR) $(TARGET)

# Ensure the build directory exists
$(BUILD_DIR):
	@if [ ! -d "$(BUILD_DIR)" ]; then mkdir "$(BUILD_DIR)"; fi

# Build the executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Compile source files to object files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -f src/*.o $(TARGET)

# Phony targets (targets that are not actual files)
.PHONY: all clean
