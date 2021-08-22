int main() {
    /* Can't have static storage class
     * on block-scope function declarations
     */
    static int foo();
    return foo();
}

static int foo() {
    return 0;
}