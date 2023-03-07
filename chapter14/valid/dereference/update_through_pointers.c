/* Test assigning to values of several types through pointers */

int main() {
    // define some variables
    unsigned int i = 2185232384u;
    signed long l = 144115196665790464l;
    double d = 1e50;

    // define pointers to those variables
    unsigned *i_ptr = &i;
    long *l_ptr = &l;
    double *d_ptr = &d;

    // assign to dereferenced pointers
    *i_ptr = 10;
    *l_ptr = 20;
    *d_ptr = 30.0;

    // check that pointed-to objects have updated values
    return (i == 10 && l == 20 && d == 30.0);

}