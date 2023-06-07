int main(void) {
    long l = -1;
    int i = -10;
    /* We should convert i to a long, then add it to l */
    l += i;
    return (l == -11);
}