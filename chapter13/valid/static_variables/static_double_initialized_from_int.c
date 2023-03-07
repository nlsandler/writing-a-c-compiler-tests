/* Test out converting initializers from an integer type to a double at compile time */

// can convert from int/uint without rounding
double a = 2147483647;
double b = 4294967295u;

/* midway point between 4611686018427388928.0 and 4611686018427389952.0
 * We round ties to even, so round this up to 4611686018427389952.0
 */
double c = 4611686018427389440l;
double c2 = 4611686018427389955l;

/* Using round-to-nearest, this rounds to 9223372036854775808 */
double d = 9223372036854775810ul;

/* This is exactly halfway between 9223372036854775808.0 and
 * 9223372036854777856.0 We round ties to even, so this
 * rounds down to 9223372036854775808.0
 */
double e = 9223372036854776832ul;

int main()
{
    // we use round-to-nearest, ties-to-even rounding
    // to convert from int to double at compile time
    return a == 2147483647. && b == 4294967295. && c == 4611686018427389952. && d == 9223372036854775808. && c == c2 && e == d;
}