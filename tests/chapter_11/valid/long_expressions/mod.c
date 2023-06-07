int main(void) {
    long a = 8589934585l;
    long b = -a % 4294967290l;
    /* Make sure mod operator works correctly when both operators
     * are too large to represent as ints
     */
    if (b == -5l) {
        return 1;
    }
    return 0;
}