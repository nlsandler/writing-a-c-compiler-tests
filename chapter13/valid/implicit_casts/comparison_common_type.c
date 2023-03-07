/* Test that we perform the usual arithmetic conversions
 * correctly on the operands of comparisons
 */
int main() {
    double d = -9007199254751228.0;
    long l = -9007199254751227l;

    /* This should return 0!
     * When we compare d to l, we implicitly
     * cast l to a double. The closest representable
     * double is -9007199254751228.0, which is equal to d,
     * not greater than d
     */
    return (d < l);
}