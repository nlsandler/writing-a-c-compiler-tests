void *malloc(unsigned long size);

int main() {
    void *buffer = malloc(100);
    char *buffer2 = (char *) buffer;
    return (buffer == buffer2);
}