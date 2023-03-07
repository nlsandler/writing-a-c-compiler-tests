/* Test addition, subtraction, multiplication, division, and negation */

int main() {

    double two = 2.0;
    double three = 3.0;
    double four = 4.0;

    // addition
    if (0.1 + 0.2 != 0.30000000000000004)
        return 0;

    // subtraction
    // test at least one operation where
    // the first operand is a variable
     if (four - 1.0 != 3.0)
        return 0;

    // multiplication
    if (0.01 * 0.3 != 0.003)
        return 0;

    // division
    // test at least one operation where
    // the second operand is a variable
    if (7.0 / two != 3.5)
        return 0;

    // test negation when source operand is a variable
    // we already test negating a constant elsewhere
    double d = 12e30;
    if (-d != 0.0 - 12e30)
        return 0;

    /* Test a more complex expression.
     * Note: all intermediate results in this expression
     * can be represented exactly, so we don't need to
     * consider the impact of rounding intermediate results.
     */

    double complex_expression = (two + three) - 127.5 * four;
    return complex_expression == -505.0;
}