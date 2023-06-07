int main(void) {
    unsigned x = 100u;
    /* if you interpret y's binary 
     * representation as a signed int,
     * its value is -2
     */
    unsigned y = 4294967294u;

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