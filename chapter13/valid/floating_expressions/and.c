int main(void) {

    /* Test && with different combinations
     * of zero and non-zero floating-point operands
     */
    int and1 = 1.0 && 2.0;
    int and2 = 0.0 && 2.0;
    int and3 = 3.0 && 0.0;

    /* also test with mix of floating-point and integer operands */
    int and4 = 0.0 && 5l;
    int and5 = -10 && 11111.1;

    /* Test cases where one operand is a variable */
    double zero = 0.0;
    int and6 = zero && 5.0;
    int and7 = 5.1 && zero;

    return and1 && !and2 && !and3 && !and4 && and5 && !and6 && !and7;
}