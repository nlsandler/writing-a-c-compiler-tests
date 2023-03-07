int main() {
    unsigned int a = 4294967294u;
    unsigned int b = 2u;
    /* a + b = 4294967296, or 2^32.
     * This is one more than the maximum value
     * an unsigned int can represent, so it should
     * wrap around to 0
     */
    return !(a + b); // Test that a + b == 0
}