/* Test conversions from double to unsigned int */
int main(void) {
    double small = 10.9;
    unsigned int small_uint = (unsigned int) small;

    // make sure we can handle a double
    // that is large enough to fit in
    // unsigned int but not int
    double big = 2147483750.5;
    unsigned int big_uint = (unsigned int) big;

    // both values should be truncated toward zeo
    return small_uint == 10u && big_uint == 2147483750u;
}