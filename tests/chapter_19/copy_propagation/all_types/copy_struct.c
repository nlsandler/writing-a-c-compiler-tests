/* Test that we can propagate copies of aggregate values */
struct s {
    int x;
    int y;
};

int callee(struct s a, struct s b) {
    return a.x == 3 && a.y == 4 && b.x == 3 && b.y == 4;
}

int target(void) {
    struct s s1 = {1, 2};
    struct s s2 = {3, 4};
    s1 = s2;  // generate s1 = s2

    // Make sure we pass the same value for both arguments.
    // We don't need to worry that register coalescing
    // will interfere with this test,
    // because s1 and s2, as structures, won't be stored in registers.
    return callee(s1, s2);
}

int main(void) {
    return target();
}