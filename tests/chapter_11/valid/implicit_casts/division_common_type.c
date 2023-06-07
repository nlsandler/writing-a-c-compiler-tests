/* Test that we perform the correct implicit conversions during division */

int main(void) {
    long l = 2147483649l;
    int i = 10;
    /* The common type of i and l is long.
     * Therefore, we should promote i to a long,
     * then divide (resulting in 214748364),
     * then convert back to an int (which can be done without
     * changing the result's value, since 214748364 is within
     * the range of int.)

     * If instead we truncated l to an int before performing division,
     * the result would be 1 / 10, or 0.
     */
    int result = l / i;
    return (result == 214748364);
}