/* Call functions wtih both even and odd numbers of stack arguments,
 * to make sure the stack is correctly aligned in both cases.
 */

int even_arguments(int a, int b, int c, int d, int e, int f, int g, int h) {
    return (a == 1 && b == 2 && c == 3 && d == 4 && e == 5
            && f == 6 && g == 7 && h == 8);
}

int odd_arguments(int a, int b, int c, int d, int e, int f, int g, int h, int i) {
    return (a == 1 && b == 2 && c == 3 && d == 4 && e == 5
            && f == 6 && g == 7 && h == 8 && i == 9);
}

int main(void) {
    /* Allocate an argument on the stack, to check that
     * we properly account for already-allocated stack space
     * when deciding how much padding to add
     */
    int x = 3;
    int result = even_arguments(1, 2, 3, 4, 5, 6, 7, 8)
                && odd_arguments(1, 2, 3, 4, 5, 6, 7, 8, 9);
    return x == 3 && result == 1;
}