/* Test conversions from double to unsigned long */
int main(void) {

    // test case where the double is smaller than LONG_MAX,
    // so result of cvttsd2siq is already correct
    double small = 2147483750.5;
    unsigned long small_long = (unsigned long) small;

    // test case where double is larger than LONG_MAX
    // so we need to adjust the results of cvttsd2siq
    double large = 3458764513821589504.0;
    unsigned long large_long = (unsigned long) large;

    // both results should be truncated toward zero
    return small_long == 2147483750ul
        && large_long == 3458764513821589504ul;

}