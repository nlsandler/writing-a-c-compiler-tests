int main(void) {
    /* -1u evaluates to UINT_MAX; -1ul evaluates to ULONG_MAX */
    if (-1u >= -1ul)
        return 0;


    /* 2^36 can't be represented as an unsigned int, 
     * so it will be promoted to an unsigned long;
     * when we compare this to -1l, we'll convert -1l to
     * an usigned long with value ULONG_MAX
     */
    if (68719476736u >= -1l)
        return 0;

    /* The same constant without the u suffix
     * is promoted to a signed long, which is greater
     * than the signed long -1
     */
    return (68719476736 > -1l);
}