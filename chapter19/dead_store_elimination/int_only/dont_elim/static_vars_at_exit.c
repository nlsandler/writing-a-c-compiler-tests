int f(void)
{
    static int i = 10;
    if (i == 5)
        return 0;
    i = 5; // not a dead store! i is live at exit
    return 1;
}

int main(void)
{
    return f() + f();
}