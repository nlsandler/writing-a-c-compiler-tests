/* It's illegal to apply bitwise |, &, or ^ to pointers */
int main(void) {
    int *x = 0;
    int *y = 0;
    return (int) (x | y);
}