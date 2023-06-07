int x = 1;

int f(void)
{
    x = 4;
    return 0;
}

int main(void)
{
    int y = x;
    f();
    return y;
}