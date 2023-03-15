int main(void) {
    unsigned long x = 1099511627775; // 2^40 - 1
    /* Test out the assembly rewrite rule for 'div' */
    return (x / 5ul == 219902325555ul);
}