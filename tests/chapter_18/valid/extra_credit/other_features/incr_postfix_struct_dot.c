/* Tests the fix for the bug reported in
 * https://github.com/nlsandler/nqcc2/issues/7
 */

struct simple {
    int x;
};

struct issue {
    unsigned long ul;
    int arr[2];
};

int main(void) {
    /* Test on a simple struct */
    struct simple s1 = {0};

    // postfix increment on arrow
    if (((struct simple*)&s1)->x++ != 0) return 1;
    if (s1.x != 1) return 2;
    if (((struct simple*)&s1)->x-- != 1) return 3;
    if (s1.x != 0) return 4;

    // postfix increment on dot
    if (s1.x++ != 0) return 5;
    if (s1.x != 1) return 6;
    if (s1.x-- != 1) return 7;
    if (s1.x != 0) return 8;

    /* Test passes the initial issue */
    struct issue s2 = {3, {2, 2}};

    if (s2.ul++ != 3) return 9;
    if (s2.ul != 4) return 10;

    return 0;
}
