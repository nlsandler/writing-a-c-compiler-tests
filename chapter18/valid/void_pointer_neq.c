void *malloc(unsigned long size);

int main() {
    void *buffer = malloc(100);
    char *buffer2 = 0;
    return (buffer != buffer2);
}