void *malloc(unsigned long size);

int main() {
    void (*ptr)[3] = malloc(3);
    return ptr == 0;
}