int indirect_update(void);

int f(int new_total)
{
    static int total = 0;
    total = new_total;
    if (total > 100)
        return 0;
    total = 10;
    indirect_update();
    return total; // can't propagate this
}

int indirect_update(void)
{
    f(101);
    return 0;
}

int main(void)
{
    return f(1);
}