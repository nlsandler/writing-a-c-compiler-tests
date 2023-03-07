/* The order in which multiple casts are applied matters */

int main() {

    unsigned int ui = 4294967200u;

    /* In this case we
     * 1. convert ui to a signed int by computing 2^32 - ui, producing -96
     * 2. signed-extend the result, which preserves the value of -96
     * Note that if we cast ui directly to a signed long, its value wouldn't change
     */
    if ((long) (signed) ui != -96l)
        return 0;

    /* In this case we
     * 1. convert ui to a signed int by computing 2^32 - ui, producing -96
     * 2. convert this signed int to an unsigned long by computing -96 + 2^64
     * Note that if we converted ui directly to an unsigned long, its value
     * wouldn't change
     */
    if ((unsigned long) (signed) ui != 18446744073709551520ul)
        return 0;

    return 1;
}