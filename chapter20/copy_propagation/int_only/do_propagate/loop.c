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
    int y = 10; // gen y = 10
    int x = y;  // gen x = y
    while (not_done())
    {
        x = something_else(); // kill x = y
        use(x);
        x = y; // gen x = y
    }

    return x; // should become "return 10"
}