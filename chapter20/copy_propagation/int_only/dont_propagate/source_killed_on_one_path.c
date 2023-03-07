int f(int src, int flag)
{
    int x = src; // generate x = src
    if (flag)
        src = 10; // kill x = src
    return x;
}

int main()
{
    return f(5, 1) + f(3, 0);
}