int flag(void)
{
    return 1;
}

int bar(void)
{
    return 4;
}

int main(void)
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