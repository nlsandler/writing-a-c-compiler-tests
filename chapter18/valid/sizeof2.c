void *malloc(unsigned long size);

int main() {
    void *buffer = malloc(100);
    return sizeof(buffer);
}