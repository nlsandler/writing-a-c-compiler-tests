/* Truncate unsigned long to int or unsigned int */

int main() {
    /* 100 can be cast to an int or unsigned int without changing its value */
    unsigned long ul = 100ul;

    if ((int) ul != 100)
        return 0;

    if (100u != (unsigned) ul)
        return 0;

    /* 4294967200 can be cast to an unsigned int without changing its value,
     * but must be reduced modulo 2^32 to cast to a signed int
     */

    ul = 4294967200ul;
    if ((unsigned) ul != 4294967200u)
        return 0;

    if (-96 != (signed) ul)
        return 0;

    /* 1152921506754330624 (2^60 + 2^31) must be reduced modulo 2^32
     * to represent as a signed or unsigned int
     */
    ul = 1152921506754330624ul;
    if (2147483648u != (unsigned) ul) // reduce to 2^31
        return 0;

    if ((signed) ul != -2147483648) // reduce to -2^31
        return 0;

    return 1;
}