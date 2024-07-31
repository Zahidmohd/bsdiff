#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bsdiff.h"
#include "bsdiff_private.h"
#include <bzlib.h>

static void log_error(void *opaque, const char *errmsg)
{
    (void)opaque;
    fprintf(stderr, "%s", errmsg);
}

// Function to initialize BZip2 compressor
static int bz2_compressor_init(void *state, struct bsdiff_stream *stream)
{
    struct bz2_compressor *enc = (struct bz2_compressor*)state;

    if (enc->initialized)
        return BSDIFF_ERROR;

    if (stream->read != NULL || stream->write == NULL || stream->flush == NULL)
        return BSDIFF_INVALID_ARG;
    enc->strm = stream;

    enc->bzstrm.bzalloc = NULL;
    enc->bzstrm.bzfree = NULL;
    enc->bzstrm.opaque = NULL;
    if (BZ2_bzCompressInit(&(enc->bzstrm), 9, 0, 30) != BZ_OK)
        return BSDIFF_ERROR;
    enc->bzstrm.avail_in = 0;
    enc->bzstrm.next_in = NULL;
    enc->bzstrm.avail_out = (unsigned int)(sizeof(enc->buf));
    enc->bzstrm.next_out = enc->buf;

    enc->bzerr = BZ_OK;

    enc->initialized = 1;

    return BSDIFF_SUCCESS;
}

// Function to write data using BZip2 compressor
static int bz2_compressor_write(void *state, const void *buffer, size_t size)
{
    struct bz2_compressor *enc = (struct bz2_compressor*)state;
    
    if (!enc->initialized)
        return BSDIFF_ERROR;
    if (enc->bzerr != BZ_OK && enc->bzerr != BZ_RUN_OK)
        return BSDIFF_ERROR;
    if (size >= UINT32_MAX)
        return BSDIFF_INVALID_ARG;
    if (size == 0)
        return BSDIFF_SUCCESS;

    enc->bzstrm.avail_in = (unsigned int)size;
    enc->bzstrm.next_in = (char*)buffer;

    while (1) {
        enc->bzerr = BZ2_bzCompress(&(enc->bzstrm), BZ_RUN);
        if (enc->bzerr != BZ_RUN_OK)
            return BSDIFF_ERROR;

        if (enc->bzstrm.avail_out == 0) {
            if (enc->strm->write(enc->strm->state, enc->buf, sizeof(enc->buf)) != BSDIFF_SUCCESS)
                return BSDIFF_ERROR;
            enc->bzstrm.next_out = enc->buf;
            enc->bzstrm.avail_out = (unsigned int)(sizeof(enc->buf));
        }

        if (enc->bzstrm.avail_in == 0)
            return BSDIFF_SUCCESS;
    }

    return BSDIFF_ERROR;
}

// Function to flush BZip2 compressor
static int bz2_compressor_flush(void *state)
{
    struct bz2_compressor *enc = (struct bz2_compressor*)state;
    size_t cb;

    if (!enc->initialized)
        return BSDIFF_ERROR;
    if (enc->bzerr != BZ_OK && enc->bzerr != BZ_RUN_OK)
        return BSDIFF_ERROR;

    while (1) {
        enc->bzerr = BZ2_bzCompress(&(enc->bzstrm), BZ_FINISH);
        if (enc->bzerr != BZ_FINISH_OK && enc->bzerr != BZ_STREAM_END)
            return BSDIFF_ERROR;

        if (enc->bzstrm.avail_out < (unsigned int)(sizeof(enc->buf))) {
            cb = sizeof(enc->buf) - enc->bzstrm.avail_out;
            if (enc->strm->write(enc->strm->state, enc->buf, cb) != BSDIFF_SUCCESS)
                return BSDIFF_ERROR;
            enc->bzstrm.avail_out = (unsigned int)(sizeof(enc->buf));
            enc->bzstrm.next_out = enc->buf;
        }

        if (enc->bzerr == BZ_STREAM_END) {
            if (enc->strm->flush(enc->strm->state) != BSDIFF_SUCCESS)
                return BSDIFF_ERROR;
            return BSDIFF_SUCCESS;
        }
    }

    return BSDIFF_ERROR;
}

// Function to close BZip2 compressor
static void bz2_compressor_close(void *state)
{
    struct bz2_compressor *enc = (struct bz2_compressor*)state;

    if (enc->initialized) {
        BZ2_bzCompressEnd(&(enc->bzstrm));
    }

    free(enc);
}

// Function to create BZip2 compressor
int bsdiff_create_bz2_compressor(struct bsdiff_compressor *enc)
{
    struct bz2_compressor *state;

    state = malloc(sizeof(struct bz2_compressor));
    if (!state)
        return BSDIFF_OUT_OF_MEMORY;
    state->initialized = 0;
    state->strm = NULL;

    memset(enc, 0, sizeof(*enc));
    enc->state = state;
    enc->init = bz2_compressor_init;
    enc->write = bz2_compressor_write;
    enc->flush = bz2_compressor_flush;
    enc->close = bz2_compressor_close;

    return BSDIFF_SUCCESS;
}

int generate_patch(const char *oldname, const char *newname, const char *patchname)
{
    int ret = 1;
    struct bsdiff_stream oldfile = { 0 }, newfile = { 0 }, patchfile = { 0 };
    struct bsdiff_ctx ctx = { 0 };
    struct bsdiff_compressor compressor = { 0 };

    ret = bsdiff_open_file_stream(BSDIFF_MODE_READ, oldname, &oldfile);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't open oldfile: %s\n", oldname);
        goto cleanup;
    }
    ret = bsdiff_open_file_stream(BSDIFF_MODE_READ, newname, &newfile);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't open newfile: %s\n", newname);
        goto cleanup;
    }
    ret = bsdiff_open_file_stream(BSDIFF_MODE_WRITE, patchname, &patchfile);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't open patchfile: %s\n", patchname);
        goto cleanup;
    }
    ret = bsdiff_create_bz2_compressor(&compressor);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't create BZ2 compressor\n");
        goto cleanup;
    }

    ctx.log_error = log_error;

    ret = bsdiff(&ctx, &oldfile, &newfile, &compressor);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "bsdiff failed: %d\n", ret);
        goto cleanup;
    }

cleanup:
    compressor.close(compressor.state);
    bsdiff_close_stream(&patchfile);
    bsdiff_close_stream(&newfile);
    bsdiff_close_stream(&oldfile);

    return ret;
}

int apply_patch(const char *oldname, const char *newname, const char *patchname)
{
    int ret = 1;
    struct bsdiff_stream oldfile = { 0 }, newfile = { 0 }, patchfile = { 0 };
    struct bsdiff_ctx ctx = { 0 };
    struct bsdiff_compressor compressor = { 0 };

    ret = bsdiff_open_file_stream(BSDIFF_MODE_READ, oldname, &oldfile);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't open oldfile: %s\n", oldname);
        goto cleanup;
    }
    ret = bsdiff_open_file_stream(BSDIFF_MODE_WRITE, newname, &newfile);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't open newfile: %s\n", newname);
        goto cleanup;
    }
    ret = bsdiff_open_file_stream(BSDIFF_MODE_READ, patchname, &patchfile);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't open patchfile: %s\n", patchname);
        goto cleanup;
    }
    ret = bsdiff_create_bz2_compressor(&compressor);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "can't create BZ2 compressor\n");
        goto cleanup;
    }

    ctx.log_error = log_error;

    ret = bspatch(&ctx, &oldfile, &newfile, &compressor);
    if (ret != BSDIFF_SUCCESS) {
        fprintf(stderr, "bspatch failed: %d\n", ret);
        goto cleanup;
    }

cleanup:
    compressor.close(compressor.state);
    bsdiff_close_stream(&patchfile);
    bsdiff_close_stream(&newfile);
    bsdiff_close_stream(&oldfile);

    return ret;
}

int main(int argc, char *argv[])
{
    if (argc != 5) {
        fprintf(stderr, "Usage: %s <oldfile> <newfile> <patchfile> <mode>\n", argv[0]);
        fprintf(stderr, "mode: 'generate' or 'apply'\n");
        return 1;
    }

    if (strcmp(argv[4], "generate") == 0) {
        return generate_patch(argv[1], argv[2], argv[3]);
    } else if (strcmp(argv[4], "apply") == 0) {
        return apply_patch(argv[1], argv[2], argv[3]);
    } else {
        fprintf(stderr, "Invalid mode: %s\n", argv[4]);
        return 1;
    }
}
