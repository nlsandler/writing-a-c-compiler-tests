/* Test conversions from double to the signed integer types */
int main(void) {

    // when truncated, d will fit in a long
    // but not an int
    double d = 2148429099.3;
    long l = (long) d;

    double e = -200000.9999;
    int i = (int) e;

    // both values should be truncated towards zero
    return l == 2148429099l && i == -200000;
}