int main(void)
{
    /* This won't match our regex
     * b/c "1.0e10" is followed by a .
     * in C standard terms, 1.0e10.0 is a
     * single preprocessing number
     */
    double d = 1.0e10.0;
    return 0;
}