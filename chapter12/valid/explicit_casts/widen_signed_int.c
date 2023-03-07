/* Test sign-extending a signed int to a long or unsigned long */

int main() {
    int i = 10;
    /* Converting a positive int to a signed long preserves its value */
    if ((signed long) i != 10l)
        return 0;

    /* Converting a positive int to an unsigned long preserves its value */
    if ((unsigned long) i != 10ul)
        return 0;

    /* Converting a negative int to a signed long preserves its value */
    i = -10;
    if ((signed long) i != -10l)
        return 0;

    /* When you convert a negative int to an unsigned long,
     * add 2^64 until it's positive
     */
    if ((unsigned long) i != 18446744073709551606ul)
        return 0;

    return 1;
}