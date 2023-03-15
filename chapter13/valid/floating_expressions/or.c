int main(void) {

    double not_zero = 2.5e-10;
    double zero = 0.0;

    // this number is so small it will be rounded to zero
    double rounded_to_zero = 1e-330;

    /* Test || with different combinations
     * of zero and non-zero floating-point operands
     */
    int or1 = not_zero || zero;
    int or2 = 0.0 || rounded_to_zero;
    int or3 = 0.0 || 25e10;

    /* Also test a mix of floating-point and integer operands */
    int or4 = 0 || rounded_to_zero; // both zero
    int or5 = 0.00005 || 0;

    return or1 && !or2 && or3 && !or4 && or5;
}