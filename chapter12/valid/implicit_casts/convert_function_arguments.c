/* Test that function arguments, including arguments put on the stack,
 * are converted to the corresponding parameter type */

int foo(long a, int b, long c, int d, long e, int f, long g, int h) {
    if (a != -1l)
        return 0;

    if (b != 2)
        return 0;

    if (c != -4294967296)
        return 0;

    if (d != -5)
        return 0;

    if (e != -101)
        return 0;

    if (f != -123)
        return 0;

    if (g != -10)
        return 0;

    if (h != 1234)
        return 0;

    return 1;
}

int main() {
    int a = -1;
    long int b = 4294967298; // 2^32 + 2, becomes 2 when converted to an int
    long c = -4294967296;
    long d = 21474836475; // 2^34 + 2^32 - 5, becomes -5 when converted to an int
    int e = -101;
    long f = -123;
    int g = -10;
    long h = -9223372036854774574; // -2^63 + 1234, becomes 1234 when converted to an int
    return foo(a, b, c, d, e, f, g, h);
}