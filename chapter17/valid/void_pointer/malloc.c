void *malloc(unsigned long size);
void free(void *ptr);

int main(void) {
    void *buffer = malloc(100);
    char *char_buffer = (char *)buffer;
    for (int i = 0; i < 100; i = i + 1) {
        char_buffer[i] = i;
    }
    char c = char_buffer[98];
    free(buffer);
    return c;
}