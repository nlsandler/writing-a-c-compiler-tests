int main() {
    unsigned long x = 100ul;
    /* This test case is identical to comparison_set_upper_bit.c,
     * except both numbers have the same value whether they're interpreted
     * as signed or unsigned values
     */
    unsigned long y = 429496729400ul;

    /* Test out every comparison code. 
     * False comparisons:
     */
    if (y < x)
        return 0;
    if (y <= x)
        return 0;
    if (x >= y)
        return 0;
    if (x > y)
        return 0;
    /* True comparisons */
    if (!(x <= y))
        return 0;
    if (!(x < y))
        return 0;
    if (!(y > x))
        return 0;
    if (!(y >= x))
        return 0;
    return (y > x);
}