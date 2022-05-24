int call()
{
    return 10;
}

int main()
{
    int x = 3;
    // make sure this loop is optimized away
    // (when we invoke both constant folding _and_ unreachable code elimination)
    while (0)
    {
        call();
        int i = 1000;
        x = x + i;
    }
    return x;
}