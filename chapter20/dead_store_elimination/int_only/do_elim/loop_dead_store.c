int f(int i)
{
    return i + 1;
}

int main()
{
    int x = 5; // dead
    int y = 3; // not
    do
    {
        x = y * 2;
        y = y + f(x);
    } while (y < 20);
    return x + y;
}