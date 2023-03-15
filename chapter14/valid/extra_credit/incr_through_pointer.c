int main(void)
{
    int x = 10;
    int *y = &x;
    ++*y;
    return x;
}