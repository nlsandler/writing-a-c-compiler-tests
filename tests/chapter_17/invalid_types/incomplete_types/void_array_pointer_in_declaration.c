void *malloc(unsigned long size);

int main(void) {
    void (*ptr)[3] = malloc(3); // array of void is illegal
    return ptr == 0;
}