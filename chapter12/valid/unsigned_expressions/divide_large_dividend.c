int main() {
    // The upper bit of x is set
    unsigned int x = 4294967294u;
    // y = x / 2
    unsigned int y = 2147483647u;

    /* This tests that we zero-extend x into EDX
     * instead of sign-extending it
     */
    return (x / y == 2);
}