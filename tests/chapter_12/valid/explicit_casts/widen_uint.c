/* Test zero-extending a uint to a long or ulong */

int main(void) {
    unsigned int ui = 4294967200u;

    /* Extending an unsigned int to a signed long preserves its value */
    if ((signed long) ui != 4294967200l)
        return 0;

    /* Extending an unsigned int to an unsigned long preserves its value */
    if ((unsigned long) ui != 4294967200ul)
        return 0;

    return 1;
}