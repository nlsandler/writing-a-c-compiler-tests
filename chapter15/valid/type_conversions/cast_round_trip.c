/* Casts between pointer types and 64-bit integer types should round trip
 * Casting a 32-bit int to a pointer and back should also round trip.
 * (Casting a pointer to a 32-bit int usually won't round trip since the
 * upper bits are discarded; we don't cover that case here.)
 */

int main() {
    /* Cast long to pointer and back */
    long x = 10;
    int *ptr = (int *) x;
    if ((long) ptr != x)
        return 0;

    /* Cast pointer to unsigned long and back */
    double d;
    double *d_ptr = &d;
    unsigned long ul = (unsigned long) d_ptr;
    if (d_ptr != (double *) ul)
        return 0;

    /* Cast one pointer type to another and back */
    d_ptr = (double *) ptr;
    if ((int *) d_ptr != ptr)
        return 0;

    /* Cast an int to a pointer and back */
    int i = 2000;
    long *l = (long *) i;
    if ((int) l != 2000)
        return 0;

    return 1;
}