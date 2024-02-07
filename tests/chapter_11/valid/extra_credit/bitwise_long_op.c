int main(void) {
    /* A long integer where the upper 32 bits are 0 and lower 32 bits are 1 */
    long lower_32_bits_set = 4294967295; // 2^32 - 1

    /* A long integer where upper 32 bits are 1 and lower 32 bits are 0 */
    long upper_32_bits_set = -1 - lower_32_bits_set;

    /* Casting a long to an int and back is equivalent to either:
     * - setting all upper bits to 1, if bit 32 is 1 (meaning the truncated int is negative)
     * or,
     * - setting all uppers bits to 0, if bit 32 is 0 (meaning the truncated int is positive)
     * Additionally, i & -1 == i for any signed integer i, whether i is a long or an int.
     * The loop below validates that these properties holds for a sample of
     * roughly 100,000,000 longs.
     */
    for (long l = 17179869184; l > 2147483648; l = l - 150) {

        int i = (int) l;
        if (i >= 0) {
            /* use bitwise "and" to zero out upper bits */
            if ((l & lower_32_bits_set) != i)
                return 1;
        } else {
            /* use bitwise "or" to set upper bits */
            if ((l | upper_32_bits_set) != i)
                return 2;
        }

        /* every bit is set in -1, so l & -1 == l */
        if ((l & -1) != l)
            return 3;
    }
    return 0; // success
}