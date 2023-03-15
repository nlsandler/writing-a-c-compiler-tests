void f(int *ptr)
{
    *ptr = 4; // not a dead store!
    return;
}

int main(void)
{
    int x = 0;
    f(&x);
    return x;
}