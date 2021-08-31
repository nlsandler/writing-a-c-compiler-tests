/* These declarations all look slightly different,
 * but they all declare 'a' as a static long, so they don't conflict.
 */
static int long a;
int static long a;
long static a;

/* These declarations all look slightly different,
 * but they all declare 'my_function' as a function
 * with three long parameters and an int return value,
 * so they don't conflict.
 */
int my_function(long a, long int b, int long c);
int my_function(long int x, int long y, long z) {
    return x + y + z;
}

int main() {
    /* Several different ways to declare local long variables */
    long x = 1l;
    long int y = 2l;
    int long z = 3l;

    /* This links to the file-scope declarations of 'a' above */
    extern long a;
    a = 4;

    /* Make sure everything has the expected value */
    return (x == 1 && y == 2 && z == 3
            && a == 4
            && my_function(x, y, z) == 6);
}