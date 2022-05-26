int foo(int *ptr)
{
    return 2;
}

int main()
{
    int x = 10;
    int *ptr = 0;
    if (0)
    {
        // need to update alias after dead code elim to recognize that
        // x is not actually aliased
        ptr = &x;
    }
    x = 5;    // this is a dead store
    foo(ptr); // why isn't 0 propagated to here?
    return 0;
}