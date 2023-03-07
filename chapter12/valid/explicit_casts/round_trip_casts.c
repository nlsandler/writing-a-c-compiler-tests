/* Converting a value to a different type, then back to the original type, 
 * does not always recover its original value
 */
int main() {
    unsigned long a = 8589934580ul; // 2^33 - 12

    /* casting to unsigned int and back reduces is equivalent to subtracting
     * 2^32, resulting in 4294967284
     */
    a = (unsigned long) (unsigned int) a;

    if (a != 4294967284ul)
        return 0;

    /* Casting to a signed int and back results in 2^64 - 12,
     * or 18446744073709551604
     */
    a = (unsigned long) (signed int) a;
    if (a != 18446744073709551604ul)
        return 0;

    return 1;
}