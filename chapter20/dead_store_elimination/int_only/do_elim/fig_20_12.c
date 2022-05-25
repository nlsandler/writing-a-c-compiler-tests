int f()
{
    return 4;
}

int g()
{
    return 5;
}

int dead_store(int flag)
{
    int x = 10; // eliminate this!
    if (flag)
    {
        x = f();
    }
    else
    {
        x = g();
    }
    return x;
}

int main()
{
    return dead_store(0) + dead_store(1);
}