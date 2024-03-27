int main(void) {
    int x = 10;
    int *ptr = &x;
    // Make sure we can use a dereferenced pointer on the left-hand side
    // of a compound assignment expression
    *ptr += 5;
    return (x == 15);
}