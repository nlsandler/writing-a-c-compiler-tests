/* Test that we perform the correct implicit conversions during addition */

int main() {
    long l = 2147483653;
    int i = 10;
    /* The common type of i and l is long, so we should
     * promote i to a long, then perform addition.
     * If we instead converted l to an int, its value would be
     * -2147483643, and the result of i + l would be -2147483633
     */
    long l2 = i + l;
    return (l2 == 2147483663l);
}