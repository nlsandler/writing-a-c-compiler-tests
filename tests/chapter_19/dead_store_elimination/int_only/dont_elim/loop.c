int f(int a, int b)
{
    return a + b;
}

int main(void)
{
    int x = 3;
    int y = 2;
    while (y < 50)
    {
        y = f(x, y);
        x = y + 2; // not dead b/c x is used in next loop iteration
    }
    return y;
}