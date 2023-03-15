int putchar(int c);

int f(int arg)
{
    int x = 76;
    // no live variables going into this basic block,
    // bu we still need to process it to learn that x is live
    if (arg)
        putchar(x);
    return 0;
}

int main(void)
{
    f(0);
    f(1);
    return 0;
}