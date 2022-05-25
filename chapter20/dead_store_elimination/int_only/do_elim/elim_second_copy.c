int g(int arg)
{
    return arg * 2;
}

int f(int arg)
{
    int x = arg + 1; // not dead
    int y = g(x);
    x = 10; // dead
    return y;
}

int main()
{
    return f(4);
}