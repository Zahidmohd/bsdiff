#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "bsdiff.h"
#include "bspatch.h"

// Define the callback functions for bsdiff
void* my_malloc(size_t size) {
    return malloc(size);
}

void my_free(void* ptr) {
    free(ptr);
}

int my_write(struct bsdiff_stream* stream, const void* buffer, int size) {
    FILE* f = (FILE*)stream->opaque;
    return fwrite(buffer, 1, size, f) == size ? 0 : -1;
}

// Define the callback function for bspatch
int my_read(const struct bspatch_stream* stream, void* buffer, int length) {
    FILE* f = (FILE*)stream->opaque;
    return fread(buffer, 1, length, f) == length ? 0 : -1;
}

// Helper function to read a file into a buffer
uint8_t* read_file(const char* path, int64_t* size) {
    FILE* f = fopen(path, "rb");
    if (!f) return NULL;

    fseek(f, 0, SEEK_END);
    *size = ftell(f);
    fseek(f, 0, SEEK_SET);

    uint8_t* buffer = malloc(*size);
    if (!buffer) {
        fclose(f);
        return NULL;
    }

    fread(buffer, 1, *size, f);
    fclose(f);

    return buffer;
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s oldfile newfile patchfile patchedfile\n", argv[0]);
        return 1;
    }

    const char* oldfile = argv[1];
    const char* newfile = argv[2];
    const char* patchfile = argv[3];
    const char* patchedfile = argv[4];

    // Read the old and new files
    int64_t oldsize, newsize;
    uint8_t* olddata = read_file(oldfile, &oldsize);
    uint8_t* newdata = read_file(newfile, &newsize);

    if (!olddata || !newdata) {
        fprintf(stderr, "Failed to read files\n");
        free(olddata);
        free(newdata);
        return 1;
    }

    // Create the patch
    FILE* pf = fopen(patchfile, "wb");
    if (!pf) {
        fprintf(stderr, "Failed to open patch file for writing\n");
        free(olddata);
        free(newdata);
        return 1;
    }

    struct bsdiff_stream bsdiff_stream = { pf, my_malloc, my_free, my_write };
    if (bsdiff(olddata, oldsize, newdata, newsize, &bsdiff_stream) != 0) {
        fprintf(stderr, "Failed to create patch\n");
        fclose(pf);
        free(olddata);
        free(newdata);
        return 1;
    }
    fclose(pf);

    // Apply the patch
    pf = fopen(patchfile, "rb");
    if (!pf) {
        fprintf(stderr, "Failed to open patch file for reading\n");
        free(olddata);
        free(newdata);
        return 1;
    }

    uint8_t* patcheddata = malloc(newsize);
    if (!patcheddata) {
        fprintf(stderr, "Failed to allocate memory for patched file\n");
        fclose(pf);
        free(olddata);
        free(newdata);
        return 1;
    }

    struct bspatch_stream bspatch_stream = { pf, my_read };
    if (bspatch(olddata, oldsize, patcheddata, newsize, &bspatch_stream) != 0) {
        fprintf(stderr, "Failed to apply patch\n");
        fclose(pf);
        free(olddata);
        free(newdata);
        free(patcheddata);
        return 1;
    }
    fclose(pf);

    // Write the patched file
    FILE* f = fopen(patchedfile, "wb");
    if (!f) {
        fprintf(stderr, "Failed to open patched file for writing\n");
        free(olddata);
        free(newdata);
        free(patcheddata);
        return 1;
    }

    fwrite(patcheddata, 1, newsize, f);
    fclose(f);

    // Clean up
    free(olddata);
    free(newdata);
    free(patcheddata);

    printf("Patch applied successfully\n");
    return 0;
}
