int flag()
{
    return 1;
}

int bar()
{
    return 4;
}

int main()
{
    int x = 1;
    // all copies reach this block, so processing its predecessor
    // won't change its incoming copies
    // but we still gotta add it to worklist
    if (flag())
    {
        x = bar();
    }
    return x;
}