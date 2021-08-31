int test_sum(long a, long b, int c, int d, int e, int f, int g, int h, long i) {
    /* Make sure the arguments passed in main weren't converted to ints */
    if (a + b < 100l) {
        return 0;
    }
    /* Check an argument that was passed on the stack too */
    if (i < 100l)
        return 0;
    return 1;
}

int main() {
    return test_sum(34359738368l, 34359738368l, 0, 0, 0, 0, 0, 0, 34359738368l);
}