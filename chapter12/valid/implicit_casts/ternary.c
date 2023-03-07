/* When we evaluate a ternary operation,
 * convert the result to the common type of both branches
 */

int main() {
    unsigned long cond = 100u;

    int i = -1;
    unsigned int ui = 10u;

    /* The common type of i and ui is unsigned int
     * (we don't consider the type of cond when we
     * determine the common type).
     * We therefore convert i to an unsigned int, 2^32 - 1,
     * which we then convert o a signed long.
     * Therefore, result will be positive. If we didn't
     * convert i to an unsigned int, result would be negative.
     */
    long result = cond ? i : ui;

    return (result > 0);
}