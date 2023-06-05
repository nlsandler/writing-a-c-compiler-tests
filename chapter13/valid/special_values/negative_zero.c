/* Test that we handle negative zero correctly */
int main(void) {
    double zero = 0.0;
    double negative_zero = -zero;

    // 0.0 and -0.0 should compare equal
    if (negative_zero != 0)
        return 0;

    // a positive number divided by negative zero is negative infinity
    if ( 1/negative_zero != -10e308 )
        return 0;

    // a negative number divided by negative zero is positive infinity
    if ( (-10)/negative_zero != 10e308)
        return 0;

    // make sure -0.0 short-circuits boolean expressions
    int fail = 0;
    -0.0 && (fail = 1);
    if (fail)
        return 0;

    return 1;
}