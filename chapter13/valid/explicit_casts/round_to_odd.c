/* Test borderline conversions from unsigned long to double */
int main(void) {
    // round_down is exactly halfway between doubles
    // 9223372036854775808.0 and 9223372036854777856.0
    // Using ties-to-even rounding, we'll round it down to
    // 9223372036854775808.0, which has an even significand
    unsigned long round_down = 9223372036854776832ul;

    // round_up is closer to 9223372036854777856.0 than
    // to 9223372036854775808.0, so we should round up.
    // our assembly code must round to odd after halving this
    // in order to avoid double rounding error
    unsigned long round_up = 9223372036854776833ul;

    double d1 = (double) round_down;
    double d2 = (double) round_up;

    return d1 == 9223372036854775808.0 &&
        d2 == 9223372036854777856.0;
}