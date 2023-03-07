int x = 1;

int f()
{
    x = 4;
    return 0;
}

int main()
{
    int y = x;
    f();
    return y;
}