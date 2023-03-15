double *ptr;

int increment_ptr(void)
{
    *ptr = *ptr + 5.0;
    return 0;
}

int main(void)
{
    double d = 10.0;
    ptr = &d;
    increment_ptr();
    return *ptr;
}