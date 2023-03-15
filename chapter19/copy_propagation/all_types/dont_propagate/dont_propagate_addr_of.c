int main(void)
{
    int x = 1;
    int y = 2;
    x = y;
    return &x == &y; // don't rewrite as &y == &y
}