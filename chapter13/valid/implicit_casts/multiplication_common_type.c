/* Test that we perform the usual arithmetic conversions
 * correctly on the operands of arithmetic operations
 */
int main() {
    /* This should promote 10 to a double,
     * calculate 10.75 * 10.0, which is 107.5,
     * and then truncate back to an int, 107.
     * It should not truncate 10.75 to 10 before
     * performing the calculation.
     */
    int i = 10.75 * 10;

    return i == 107;
}