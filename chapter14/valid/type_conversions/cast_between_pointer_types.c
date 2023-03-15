/* Test explicitly casting between pointer types */
int main(void)
{
    /* You can cast a null pointer to any pointer type and the result is still a null pointer */
    long *long_ptr = 0;
    double *dbl_ptr = (double *)long_ptr;
    unsigned int *int_ptr = (unsigned int *)long_ptr;
    int **ptr_ptr = (int **)long_ptr;

    if (long_ptr || dbl_ptr || int_ptr || ptr_ptr)
        return 0;

    // conversions between pointer types should round trip
    long l = -1;
    long_ptr = &l;
    dbl_ptr = (double *)long_ptr;
    long *other_long_ptr = (long *)dbl_ptr;
    return *other_long_ptr == -1;
}