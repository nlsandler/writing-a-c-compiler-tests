/* Test conversions between signed and unsigned types of the same size */

int main() {
    int x = 10;
    unsigned int y = (unsigned) x;

    /* Converting a positive signed int to an unsigned int preserves its value */
    if (y != 10u)
        return 0;

    /* If an unsigned int is within the range of signed int,
     * converting it to a signed int preserves its value
     */
    if ((signed) y != 10)
        return 0;

    /* Converting a negative signed long -x to an unsigned long
     * results in 2^64 - x
     */
    long a = -1000;
    unsigned long b = (unsigned long) a;
    if (b != 18446744073709550616ul)
        return 0;

    /* If an unsigned long is too large for a long to represent,
     * reduce it modulo 2^64 until it's in range.
     */
    if ((long) b != -1000)
        return 0;

    return 1;
}