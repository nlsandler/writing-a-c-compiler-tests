/* Test that we round constants to infinity
 * if they're too large to represent as finite doubles
 */
int main(void) {
    /* These two values are larger than the largest finite double,
     * so they should be converted to infinity
     */
    double inf1 = 2e308;
    double inf2 = 11e330;
    /* This should round to the largest finite double */
    double very_large = 1.79E308;

    if (inf1 != inf2)
        return 0;

    if (inf1 <= very_large)
        return 0;

    return 1;
}