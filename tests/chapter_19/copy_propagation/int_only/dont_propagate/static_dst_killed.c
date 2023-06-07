int x;

int update_x(void)
{
    x = 4;
    return 0;
}

int main(void)
{
    x = 3;
    update_x();
    return x; // can't propagte b/c it's static
}