/* Test conversions from unsigned long to double */

int main(void) {
    // convert a value that's already in the range of signed long
    unsigned long small = 138512825844ul;
    double small_double = (double) small;

    // convert a value that's outside the range of signed long
    unsigned long big = 10223372036854775816ul;
    double big_double = (double) big;

    return (small_double == 138512825844.0 && big_double == 10223372036854775808.0);

}