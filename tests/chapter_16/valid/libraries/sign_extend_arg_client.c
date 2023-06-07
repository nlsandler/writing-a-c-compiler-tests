/* NOTE: due to ABI incompatibility between our compiler and clang,
 * this should succeed if we compile lib with clang w/out optimizations,
 * fail if we compile lib with clang w/ optimizations,
 * succeed if we compile lib with GCC or ICC
 */

int narrow_params(char a, char b);

int compare_longs(long a, long b)
{
    return a == b;
}

int main(void)
{
    /* pass values w/ upper bytes set in RDI & RSI */
    if (compare_longs(-1, -2))
        return 0;
    /* now pass chars in RDI + RSI */
    return narrow_params(1, 2) == 3;
}