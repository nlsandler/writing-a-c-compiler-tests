int not_done()
{
    static int i = 10;
    i = i - 1;
    return i;
}

int something_else()
{
    return 5;
}

int use(int i)
{
    return i + 1;
}

int main()
{
    int y = 10;
    int x = y;
    while (not_done())
    {
        x = something_else();
        use(x);
        x = y;
    }

    return x; // should become "return 10"
}