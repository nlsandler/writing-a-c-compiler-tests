int foo(void)
{
    return 10;
}

int main(void)
{
    int x = foo();
    int y = x; // generate y = x
    x = 4;     // kill y = x
    return y;  // can't replace y with x here
}