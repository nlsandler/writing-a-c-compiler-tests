int flag()
{
    return 0;
}

int number()
{
    return 3;
}

int main()
{
    int x;
    if (flag())
        x = 10;
    else
        x = number();
    // one predecessor contains copy x = 10, other predecessor contains no copies to x,
    // so no copies reach start of this block
    return x;
}