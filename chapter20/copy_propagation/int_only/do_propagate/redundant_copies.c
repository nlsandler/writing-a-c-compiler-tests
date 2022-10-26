int foo()
{
    return 3;
}

int main()
{
    int y = foo();
    int x = y;
    y = x;
    // make sure value we move into eax (if any) is same value we moved out
    // and if we move eax into dst, no subsequent updates to dst (i.e. we get rid of y = x)
    return y;
}