
# bsdiff/bspatch Example

This project demonstrates how to use the `bsdiff` and `bspatch` libraries for creating and applying binary patches. The original algorithm and implementation were developed by Colin Percival.

## Overview

The project consists of:
- `bsdiff`: A library for generating binary patches.
- `bspatch`: A library for applying binary patches.

These libraries are modified to eliminate external dependencies and provide a simple interface to the core functionality. The project includes a `main.c` file that serves as an example for using these libraries.

## Directory Structure

- project/
  - ├── src/
     - ├── bsdiff.c
     - ├── bspatch.c
     -  └── main.c
   - ├── include/
      -  ├── bsdiff.h
      - └── bspatch.h
   - ├── build/
   - ├── Makefile
   - ├── old_file_0.bin
   - ├── new_file_0.bin
   - └── README.md


## Building the Project

### Using `make`

1. Ensure you have `make` installed on your system.
2. Navigate to the root of your project directory.
3. Run the following command to build the project:

   make

   This will compile the source files and create the executable `myprogram` in the `build` directory.

### Manual Compilation

If you don't have `make` installed, you can manually compile the project using gcc:

1. Navigate to the root of your project directory.
2. Create the `build` directory if it doesn't exist:
   mkdir build

3. Compile the source files:
   - `gcc -std=c99 -Wall -Iinclude -c src/main.c -o build/main.o`
   - `gcc -std=c99 -Wall -Iinclude -c src/bsdiff.c -o build/bsdiff.o`
   - `gcc -std=c99 -Wall -Iinclude -c src/bspatch.c -o build/bspatch.o`

4. Link the object files to create the executable:
   `gcc -std=c99 -Wall -Iinclude -o build/myprogram build/main.o build/bsdiff.o build/bspatch.o`

## Running the Program

The program expects four arguments:

1. `oldfile`: The original file.
2. `newfile`: The new file you want to create a patch for.
3. `patchfile`: The patch file to be created.
4. `patchedfile`: The resulting file after applying the patch to `oldfile`.

To run the program, use the following command:

`./build/myprogram oldfile newfile patchfile patchedfile`

### Example

`./build/myprogram old_file_0.bin new_file_0.bin file_0.patch patched_file_0.bin`

This command will:
1. Create a patch (`file_0.patch`) from `old_file_0.bin` and `new_file_0.bin`.
2. Apply the patch to `old_file_0.bin` to create `new_file_recreated_0.bin`.