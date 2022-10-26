int foo()
{
    return 3;
}

int main()
{
    int x = 2;
    x = foo();
    x = 2;
    return x; // look for movl $2, %eax
}