int main(void) {
    /* Negating -1 is equivalent to computing 0 - 1.
     * According to the rules for unsigned wraparound,
     * this results in ULONG_MAX
     */
    unsigned long x = -1ul;
    // This is ULONG_MAX - 1
    unsigned long y = 18446744073709551615u;
    return x == y;
}