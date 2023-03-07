double *ptr = 0;

void save_ptr(double *to_save)
{
    ptr = to_save;
}

void update_ptr()
{
    *ptr = 2.0;
}

int main()
{
    double d = 10.0;
    double *ptr = &d;
    double *another_ptr = (double *)(int *)ptr;
    save_ptr(another_ptr);
    d = 1.0;
    update_ptr();
    return d;
}