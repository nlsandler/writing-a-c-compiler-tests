/* Test conversions from unsigned int to double */

int main() {
    unsigned int small = 1000u;
    double small_double = (double) small;

    // make sure we can convert a uint that's
    // larger than INT_MAX to a double
    unsigned int large = 4294967200u;
    double large_double = (double) large;

    return (small_double == 1000.0 && large_double == 4294967200.0);
}