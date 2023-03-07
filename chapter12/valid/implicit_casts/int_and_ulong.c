/* When performing an operation on two different types,
 * where the unsigned type is an equal or higher rank,
 * convert the signed value to the unsigned type
 */

int main() {
    /* This value is 2^64 - 10,
     * which is too large to represent as an unsigned int
     * or signed long
     */
    unsigned long ul =  18446744073709551606ul;

    // this will be converted to 2^64 - 1
    int i = -1;

    return (i > ul);
}