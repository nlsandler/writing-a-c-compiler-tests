/* Test conversions from signed integer types to double */

int main(void) {
    int i = -100000;
    double d = (double) i;

    // Cast a long to the closest representable double,
    // which is -9007199254751228.
    // NOTE: most of our type conversion tests cast variables to double.
    // Here we include a test to cast a constant to double,
    // to make sure we rewrite cvtsi2sd if its operand is a constant
    double d2 = (double) -9007199254751227l;

    return (d == -100000.0 && d2 == -9007199254751228.0);
}