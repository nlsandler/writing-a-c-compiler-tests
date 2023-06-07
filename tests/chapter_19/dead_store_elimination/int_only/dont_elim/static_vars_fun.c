int x = 100;

int get_x(void)
{
    return x;
}

int main(void)
{
    x = 5; // don't eliminate this!
    return get_x();
}