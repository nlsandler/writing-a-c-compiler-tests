/* Test out converting initializers from an integer type to a double at compile time */

/* Using round-to-nearest, this rounds to 9223372036854775808 */
double d = 9223372036854775810ul;

/* This is exactly halfway between 9223372036854775808.0 and
 * 9223372036854777856.0 We round ties to even, so this
 * rounds down to 9223372036854775808.0
 */
double e = 9223372036854776832ul;

int main() {
    // we use round-to-nearest, ties-to-even rounding
    // to convert from int to double at compile time
    return d == 9223372036854775808. && e == d;
}