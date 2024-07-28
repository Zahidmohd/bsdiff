#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <bzlib.h>
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

// Helper function to write a buffer to a file
int write_file(const char* path, const uint8_t* buffer, int64_t size) {
    FILE* f = fopen(path, "wb");
    if (!f) return -1;

    if (fwrite(buffer, 1, size, f) != size) {
        fclose(f);
        return -1;
    }

    fclose(f);
    return 0;
}

// Helper function to compress a buffer using BZip2
int compress_bzip2(const uint8_t* input, int64_t input_size, uint8_t** output, int64_t* output_size) {
    unsigned int dest_len = input_size + (input_size / 100) + 600; // BZip2 recommendation
    *output = malloc(dest_len);
    if (!*output) return -1;

    int result = BZ2_bzBuffToBuffCompress((char*)*output, &dest_len, (char*)input, input_size, 9, 0, 0);
    if (result != BZ_OK) {
        free(*output);
        return -1;
    }

    *output_size = dest_len;
    return 0;
}

// Helper function to decompress a buffer using BZip2
int decompress_bzip2(const uint8_t* input, int64_t input_size, uint8_t** output, int64_t output_size) {
    *output = malloc(output_size);
    if (!*output) return -1;

    unsigned int dest_len = output_size;
    int result = BZ2_bzBuffToBuffDecompress((char*)*output, &dest_len, (char*)input, input_size, 0, 0);
    if (result != BZ_OK) {
        free(*output);
        return -1;
    }

    return 0;
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

    // Read the patch file into a buffer
    int64_t patch_size;
    uint8_t* patch_data = read_file(patchfile, &patch_size);
    if (!patch_data) {
        fprintf(stderr, "Failed to read patch file\n");
        free(olddata);
        free(newdata);
        return 1;
    }

    // Compress the patch data
    uint8_t* compressed_patch_data;
    int64_t compressed_patch_size;
    if (compress_bzip2(patch_data, patch_size, &compressed_patch_data, &compressed_patch_size) != 0) {
        fprintf(stderr, "Failed to compress patch file\n");
        free(olddata);
        free(newdata);
        free(patch_data);
        return 1;
    }

    free(patch_data);

    // Write the compressed patch data to the patch file
    if (write_file(patchfile, compressed_patch_data, compressed_patch_size) != 0) {
        fprintf(stderr, "Failed to write compressed patch file\n");
        free(olddata);
        free(newdata);
        free(compressed_patch_data);
        return 1;
    }

    free(compressed_patch_data);

    // Apply the patch
    pf = fopen(patchfile, "rb");
    if (!pf) {
        fprintf(stderr, "Failed to open patch file for reading\n");
        free(olddata);
        free(newdata);
        return 1;
    }

    // Read the compressed patch file into a buffer
    uint8_t* compressed_patch_data_read = read_file(patchfile, &compressed_patch_size);
    if (!compressed_patch_data_read) {
        fprintf(stderr, "Failed to read compressed patch file\n");
        fclose(pf);
        free(olddata);
        free(newdata);
        return 1;
    }
    fclose(pf);

    // Decompress the patch data
    uint8_t* decompressed_patch_data;
    if (decompress_bzip2(compressed_patch_data_read, compressed_patch_size, &decompressed_patch_data, patch_size) != 0) {
        fprintf(stderr, "Failed to decompress patch file\n");
        free(olddata);
        free(newdata);
        free(compressed_patch_data_read);
        return 1;
    }

    free(compressed_patch_data_read);

    // Apply the decompressed patch
    uint8_t* patcheddata = malloc(newsize);
    if (!patcheddata) {
        fprintf(stderr, "Failed to allocate memory for patched file\n");
        free(olddata);
        free(newdata);
        free(decompressed_patch_data);
        return 1;
    }

    struct bspatch_stream bspatch_stream = { decompressed_patch_data, my_read };
    if (bspatch(olddata, oldsize, patcheddata, newsize, &bspatch_stream) != 0) {
        fprintf(stderr, "Failed to apply patch\n");
        free(olddata);
        free(newdata);
        free(decompressed_patch_data);
        free(patcheddata);
        return 1;
    }

    free(decompressed_patch_data);

    // Write the patched file
    if (write_file(patchedfile, patcheddata, newsize) != 0) {
        fprintf(stderr, "Failed to write patched file\n");
        free(olddata);
        free(newdata);
        free(patcheddata);
        return 1;
    }

    // Clean up
    free(olddata);
    free(newdata);
    free(patcheddata);

    printf("Patch applied successfully\n");
    return 0;
}
