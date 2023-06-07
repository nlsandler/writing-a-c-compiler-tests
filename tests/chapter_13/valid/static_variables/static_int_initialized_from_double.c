/* Test out converting an initializer from a double to an int at compile time */

// this is converted to 4
static int i = 4.9;

int unsigned u = 42949.672923E5;

// this token is first converted to a double w/ value 4611686018427389952.0,
// then truncated down to long 4611686018427389952
long l = 4611686018427389440.;

unsigned long ul = 18446744073709549568.;

int main(void)
{
    return i == 4 && u == 4294967292u && l == 4611686018427389952l && ul == 18446744073709549568ul;
}