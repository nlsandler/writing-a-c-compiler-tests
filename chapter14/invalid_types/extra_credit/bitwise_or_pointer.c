/* It's illegal to apply bitwise |, &, or ^ to pointers */
int main() {
    int *x = 0;
    int *y = 0;
    return (int) (x | y);
}