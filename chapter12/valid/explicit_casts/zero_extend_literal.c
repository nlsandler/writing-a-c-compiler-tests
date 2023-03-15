int main(void) {
    /* Zero-extend 4294967200
     * from an unsigned int to an unsigned long
     * to test the assembly rewrite rule for MovZeroExtend
     */
    unsigned long x = (unsigned long) 4294967200u;
    return (x == 4294967200ul);
}