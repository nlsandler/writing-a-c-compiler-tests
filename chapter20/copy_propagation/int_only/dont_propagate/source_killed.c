int foo()
{
    return 10;
}

int main()
{
    int x = foo();
    int y = x; // generate y = x
    int x = 4; // kill y = x
    return y;  // can't replace y with x here
}