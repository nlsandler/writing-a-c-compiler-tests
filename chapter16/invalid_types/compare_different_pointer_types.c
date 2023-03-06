int main()
{
    long x = 10;
    long *ptr = &x + 1;
    long(*array_ptr)[10] = &x;
    // cannot compare array_ptr to ptr because they have different types
    return array_ptr < ptr;
}