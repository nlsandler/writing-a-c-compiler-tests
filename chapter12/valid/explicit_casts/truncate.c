int main() {
    /* If a long is already in the range of 'int',
     * truncation doesn't change its value.
     */
    long l = 10l;
    int i = (int) l;
    if (i != 10)
        return 0;

    /* Truncating a negative int also preserves its value */
    l = -10l;
    i = (int) l;
    if (i != -10)
        return 0;

    /* If a long is outside the range of int,
     * subtract 2^32 until it's in range
     */
    l = 17179869189l; // 2^34 + 5
    i = (int) l;
    if (i != 5)
        return 0;

    /* If a negative long is outside the range of int,
     * add 2^32 until it's in range
     */
    l = -17179869179l; // (-2^34) + 5
    i = (int) l;
    if (i != 5)
        return 0;

    return 1;
}