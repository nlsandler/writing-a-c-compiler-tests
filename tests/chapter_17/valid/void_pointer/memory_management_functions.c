void *malloc(unsigned long size);
void *realloc(void *ptr, unsigned long size);
void *calloc(unsigned long nmemb, unsigned long size);
void *aligned_alloc(unsigned long alignment, unsigned long size);
void free(void *ptr);

int puts(char *c); // for error messages

int main(void) {
    // allocate a buffer with malloc and populate it
    char *char_buffer = malloc(50);
    for (int i = 0; i < 50; i = i + 1) {
        char_buffer[i] = i;
    }

    // reallocate buffer
    char *char_buffer2 = realloc(char_buffer, 100);
    // we made it bigger, so update a value beyond the bounds of the old buffer
    // (whose value is undefined to start)
    char_buffer2[75] = 11;
    // make sure the contents are the same
    for (int i = 0; i < 50; i = i + 1) {
        if ( char_buffer2[i] != i) {
            puts("Bad contents in realloc'd buffer");
            return i + 1;
        }
    }
    if (char_buffer2[75] != 11) {
        puts("Bad value in byte 75 of realloc'd buffer");
        return 51;
    }

    free(char_buffer2);

    // allocate a new buffer with calloc
    double *double_buffer = calloc(10, sizeof(double));
    for (int i = 0; i < 10; i = i + 1) {
        if (double_buffer[i]) {
            puts("Non-zero value in calloc'd buffer");
            return 100 + i;
        }
    }
    free(double_buffer);

    // try out aligned alloc
    char_buffer = aligned_alloc(256, 256);
    // make sure it's 256 byte-aligned
    if ((unsigned long) char_buffer % 256) {
        puts("Got misaligned buffer from aligned_alloc.");
        return 201;
    }
    free(char_buffer);
    return 0;
}