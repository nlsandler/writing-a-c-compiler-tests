/* Make sure we can handle adding, subtracting,
 * and multiplying by constants that are outside
 * the range of int; this tests our assembly rewrite rules.
 */

int main(void) {
    long x = 5l;

    /* Add a large constant to a variable */
    x = x + 4294967290l;
    if (x != 4294967295l)
        return 0;

    /* Subtract a large constant from a variable */
    x = x - 4294967290l;
    if (x != 5l)
        return 0;

    /* Multiply a variable by a large constant */
    x = x * 4294967290l;
    if (x != 21474836450l)
        return 0;

    return 1;
}