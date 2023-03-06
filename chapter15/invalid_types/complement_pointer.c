/* It's illegal to take the bitwise complement of a pointer. */
int main() {
    int *x = 0;
    return (int) ~x;
}