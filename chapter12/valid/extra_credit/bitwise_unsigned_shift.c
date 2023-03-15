/* Bit-shift operations do not perform the usual arithmetic conversions. */

int main(void) {
    unsigned int ui = -1u; // 2^32 - 1, or 4294967295

    /* shifting right by 2 is like subtracting 3.
     * note that we don't cast ui to a long first
     */
    return ((ui << 2l) == 4294967292);
}