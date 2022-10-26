int flag()
{
    return 0;
}

int add(int a, int b)
{
    return a + b;
}

int main()
{
    int x;
    int y;
    if (flag())
    {
        y = 10;
        x = y;
    }
    else
    {
        y = 20;
        x = y;
    }
    // x = y reaches here, though with different values of y
    // compare to Figure 20-6
    // make sure we copy same value into edi and esi (or copy one to the other)
    // NOTE: can also accomplish this (and most copy prop-specific tests) w/ copy coalescing
    // combine w/ constant folding to verify?
    return add(x, y);
}