/* Truncate from signed long to unsigned int */

int main(void) {

    /* 100 is in the range of unsigned int,
     * so truncating it to an unsigned int
     * will preserve its value
     */
    long l = 100l;
    if ((unsigned) l != 100u)
        return 0;

    /* -9223372036854774574 is outside the range of unsigned int,
     * so add 2^32 to bring it within range */
    l = -9223372036854774574l; // -2^63 + 1234
    if ((unsigned) l != 1234)
        return 0;


    return 1;
}