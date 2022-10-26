int f(int arg)
{
    static int i;
    if (arg < 0)
        return i;
    i = 5; // this is dead
    i = arg;
    return i;
}

int main()
{
    return f(2) + f(-1);
}