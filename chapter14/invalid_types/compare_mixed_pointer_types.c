/* It's illegal to compare two different pointer types */
int main() {
    int *x = 0ul;
    unsigned *y = 0ul;
    return x == y;
}