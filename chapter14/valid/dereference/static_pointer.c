double *ptr;

int increment_ptr()
{
    *ptr = *ptr + 5.0;
    return 0;
}

int main()
{
    double d = 10.0;
    ptr = &d;
    increment_ptr();
    return *ptr;
}