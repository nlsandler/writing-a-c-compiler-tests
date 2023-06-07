int main(void) {
    unsigned x = 100u;
    /* if you interpret y's binary 
     * representation as a signed int,
     * its value is -2
    */
    unsigned y = 4294967294u;

    /* If we're performing unsigned division,
     * this result is 0. If we performed signed
     * division it would be -50.
     */
    return (x / y == 0u);
}