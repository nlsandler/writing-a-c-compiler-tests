int wide_params(int a, int b)
{
    return a + b;
}

/* If we're using clang and theres' garbage in a + b,
 * this will gave the wrong answer!
 * NOTE: only w/ -O enabled, this will require special case handling in test script
 * */
int narrow_params(char a, char b)
{
    return wide_params(a, b);
}