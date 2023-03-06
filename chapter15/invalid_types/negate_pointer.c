/* It's illegal to negate a pointer */
int main() {
    int *x = 0;
    return (int) -x;
}