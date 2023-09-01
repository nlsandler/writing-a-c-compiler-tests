/* Converting a value to a different type, then back to the original type,
 * does not always recover its original value
 */

// start with a global variable so we can't optimize away casts in Part III
unsigned long a = 8589934580ul; // 2^33 - 12

int main(void) {

    /* casting to unsigned int and back reduces is equivalent to subtracting
     * 2^32, resulting in 4294967284
     */
    unsigned long b = (unsigned long) (unsigned int) a;

    if (b != 4294967284ul)
        return 1;

    /* Casting to a signed int and back results in 2^64 - 12,
     * or 18446744073709551604
     */
    b = (unsigned long) (signed int) a;
    if (b != 18446744073709551604ul)
        return 2;

    return 0;
}