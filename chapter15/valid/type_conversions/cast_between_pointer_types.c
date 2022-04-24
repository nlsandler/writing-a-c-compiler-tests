/* Test explicitly casting between pointer types */
int main() {
    /* The bits stored in l are all zeros, so they have the value zero
     * when interpreted as any arithmetic or pointer type
     */
    long l = 0;
    long *long_ptr = &l;
    double *dbl_ptr = (double *) &l;
    unsigned int *int_ptr = (unsigned int *) long_ptr;
    int **ptr_ptr = (int **) &l;

    if (*long_ptr != 0 || *dbl_ptr != 0 || *int_ptr != 0 || *ptr_ptr != 0)
        return 0;

    double d = -0.0;
    unsigned long *ul_ptr = (unsigned long *) &d;

    // the bit representation of d is a leading one followed by all zeros.
    // if we reinterpret these bytes as an unsigned long their value is 2^63
    return (*ul_ptr == 9223372036854775808ul);
}