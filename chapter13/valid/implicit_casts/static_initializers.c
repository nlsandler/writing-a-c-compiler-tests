/* Make sure static initializers are set to the correct
 * implicitly-converted value at program startup
 */

/* This should be initialized to 4294967246,
 * or 2^32 - 50
 */
unsigned int ui = -50;

/* This should be initialized to 18446744073709551566,
 * or 2^64 - 50
 */

unsigned long ul = -50;

/* This should be initialized to -2147483646,
 * or 2147483650 - 2^32
 */
int i = 2147483650;

/* This should be initialized to -9223372036854775716,
 * or 9223372036854775900 - 2^64
 */
long l = 9223372036854775900u;

int main() {
    if (ui != 4294967246u)
        return 0;
    if (ul != 18446744073709551566ul)
        return 0;
    if (i != -2147483646)
        return 0;
    if (l != -9223372036854775716l)
        return 0;

    return 1;
}