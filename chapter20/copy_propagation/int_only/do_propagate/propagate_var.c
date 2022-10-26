int foo()
{
    return 3;
}

int main()
{
    int x = foo();
    int y = x;
    // look for: value copied out of eax right after foo is copied back into eax before ret
    // OR eax not updated at all
    return y;
}