/* Test that we can parse a variety of function and variable declarators */

/* Multiple declarations of the function 'return_3'
 * These declarations all have the same type so they don't conflict.
 */
int return_3(void);
int(return_3(void));
int(return_3)(void);
int((return_3))(void)
{
    return 3;
}

/* Multiple declarations of the function 'two_pointers'
 * These declarations all have the same type so they don't conflict
 */
long l = 100;
long *two_pointers(double val, double *ptr)
{
    *ptr = val;
    return &l;
}
long(*two_pointers(double val, double(*d)));
long *(two_pointers)(double val, double *(d));
long *(two_pointers)(double val, double(*(d)));

/* Multiple declarations of the function 'pointers_to_pointers'
 * These declarations all have the same type so they don't conflict
 */
unsigned **pointers_to_pointers(int **p)
{
    static unsigned u;
    static unsigned *u_ptr;
    u_ptr = &u;
    u = **p;
    return &u_ptr;
}
unsigned(**(pointers_to_pointers(int *(*p))));
unsigned *(*pointers_to_pointers(int(**p)));
unsigned(*(*((pointers_to_pointers)(int(*(*(p)))))));

int main(void)
{
    /* Declare some variables using a variety of declarators */
    int i = 0;
    int(*i_ptr) = &i;
    int(**ptr_to_iptr) = &i_ptr;

    double(d1) = 0.0;
    double d2 = 10.0;

    double *(d_ptr) = &d1;

    long(*(l_ptr));

    unsigned *(*(ptr_to_uptr));

    /* Use functions and variables we just declared */
    i = return_3(); // assign 3 to i
    if (i != 3)
        return 0;

    // call two_pointers and validate the results
    l_ptr = two_pointers(d2, d_ptr);
    if (*l_ptr != 100 || *d_ptr != 10.0)
        return 0;

    // call pointers_to_pointers and validate the results
    ptr_to_uptr = pointers_to_pointers(ptr_to_iptr);

    return **ptr_to_uptr == 3;
}