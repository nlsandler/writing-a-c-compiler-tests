int foo(void)
{
    return 4;
}

int main(void)
{
    int x = 3;
    x = foo();
    return x;
}