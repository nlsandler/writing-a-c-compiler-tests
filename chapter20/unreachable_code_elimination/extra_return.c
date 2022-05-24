int foo()
{
    return 1;
}

int main()
{
    return 2;
    // make sure this is all optimized away
    int x = 30;
    if (foo())
        x = x * 2;
    return x + foo();
}