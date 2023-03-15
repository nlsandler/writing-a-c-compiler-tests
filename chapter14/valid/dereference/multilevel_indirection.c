/* Test that we correctly handle pointers to pointers */
int main(void) {
    double d = 10.0;
    double *d_ptr = &d;
    double **d_ptr_ptr = &d_ptr;
    double ***d_ptr_ptr_ptr = &d_ptr_ptr;

    // read value of d through multiple levels of indirection
    if (!(d == 10.0 && *d_ptr == 10.0 && **d_ptr_ptr == 10.0
            && ***d_ptr_ptr_ptr == 10.0))
        return 0;

    // read address of d through multiple levels of indirection
    if (!(&d == d_ptr && *d_ptr_ptr == d_ptr && **d_ptr_ptr_ptr == d_ptr))
        return 0;

    // update value of d through multiple levels of indirection
    ***d_ptr_ptr_ptr = 5.0;
    if (!(d == 5.0 && *d_ptr == 5.0 && **d_ptr_ptr == 5.0
            && ***d_ptr_ptr_ptr == 5.0))
        return 0;

    // update addresses at different levels of indirection
    double d2 = 1.0;

    // make both d2_ptr and d2_ptr2 point to same variable, d
    double *d2_ptr = &d2;
    double *d2_ptr2 = d2_ptr;
    double **d2_ptr_ptr = &d2_ptr;

    *d_ptr_ptr_ptr = d2_ptr_ptr;
    if (!(*d_ptr_ptr_ptr == d2_ptr_ptr && **d_ptr_ptr_ptr == d2_ptr
        && **d_ptr_ptr_ptr == d2_ptr2 && ***d_ptr_ptr_ptr == d2))
        return 0;

    // even though d2_ptr and d2_ptr2 have the same value,
    // they don't have the same address;
    // d2_ptr_ptr points to d2_ptr but not d2_ptrs
    if (d2_ptr_ptr == &d2_ptr2)
        return 0;

    // changing the value of d2_ptr also changes *d2_ptr2 and **d_ptr_ptr_ptr
    d2_ptr = d_ptr;

    if (!(**d_ptr_ptr_ptr == d_ptr && *d2_ptr_ptr == d_ptr
        && **d_ptr_ptr_ptr != d2_ptr2 && ***d_ptr_ptr_ptr == 5.0))
        return 0;

    return 1;
}