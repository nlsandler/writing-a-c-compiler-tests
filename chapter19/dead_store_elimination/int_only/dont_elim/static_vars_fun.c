int x = 100;

int get_x()
{
    return x;
}

int main()
{
    x = 5; // don't eliminate this!
    return get_x();
}