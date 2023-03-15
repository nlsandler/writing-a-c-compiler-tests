/* It's illegal to negate a pointer */
int main(void) {
    int *x = 0;
    return (int) -x;
}