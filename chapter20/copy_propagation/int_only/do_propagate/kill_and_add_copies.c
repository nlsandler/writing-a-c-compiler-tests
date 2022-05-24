static int x = 0; // make x static so it's not impacted by dead store elim

int set_x()
{
    x = 4;
    return 1;
}

int use(int a, int b)
{
    return a + b;
}

int main()
{
    set_x();
    int y = x; // gen y = x;
    x = 10;    // kill y = x, gen x = 10
    // look for:
    // movl $10, %edi
    return use(x, y); // becomes use(10, y)
}