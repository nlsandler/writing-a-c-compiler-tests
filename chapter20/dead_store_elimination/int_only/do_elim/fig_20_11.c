int f(int arg)
{
    // run w/ only DSE is enabled, and make sure it's correct
    // (we can't eliminate assignment x = 10
    // b/c it may be used in 'return x')
    // run w/ DSE + copy prop and make sure it _is_ enabled
    int x = 10;
    if (arg)
        return x;
    return 0;
}

int main()
{
    return f(0) + f(1);
}