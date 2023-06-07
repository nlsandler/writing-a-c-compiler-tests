int main(void) {
    /* a variable can't have more than one storage class */
    static extern foo = 0;
    return foo;
}