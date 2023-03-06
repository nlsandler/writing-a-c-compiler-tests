int main() {
    int i = -100;
    long l = 4294967296; // 2^32

    /* Make sure we convert i to a long instead of converting l to an int.
     * If we convert l to an int its value will be -2147483648,
     * which is smaller than -100.
     */     
    if (i >= l)
        return 0;

    return 1;
}