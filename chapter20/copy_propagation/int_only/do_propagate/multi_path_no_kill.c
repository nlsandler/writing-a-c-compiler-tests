int flag()
{
    return 1;
}

int do_something()
{
    return 5;
}

int main()
{
    int x = 3;
    if (flag())
        do_something();
    return x; // look for movl $3, %eax
}