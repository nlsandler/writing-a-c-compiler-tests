int foo(int i)
{
    return i == 4;
}

int main()
{
    int y = 3;
    int x;
    do
    {
        x = foo(y);
        y = 4;
    } while (x);
    return y; // should become return 4
}