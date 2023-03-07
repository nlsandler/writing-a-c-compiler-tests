/* Test reading values of several types through pointers */
int main() {

    // define some variables
    int i = -100;
    unsigned long ul = 13835058055282163712ul;
    double d = 3.5;

    //define some pointers to those variables
    int *i_ptr = &i;
    unsigned long *ul_ptr = &ul;
    double *d_ptr = &d;

    // dereference each pointer and read value
    if (*i_ptr != -100 || *ul_ptr != 13835058055282163712ul || *d_ptr != 3.5)
        return 0;

    // update values, and make sure we can read updated values through pointers
    i = 12;
    ul = 1000;
    d = -000.001;

    if (*i_ptr != 12 || *ul_ptr != 1000 || *d_ptr != -000.001)
        return 0;

    // assign new values to the pointers, then make sure dereferencing them
    // results in the values of the new objects they point to
    int i2 = 1;
    unsigned long ul2 = 144115196665790464ul;
    double d2 = -33.3;

    i_ptr = &i2;
    ul_ptr = &ul2;
    d_ptr = &d2;

    if (*i_ptr != 1 || *ul_ptr != 144115196665790464ul || *d_ptr != -33.3)
        return 0;

    return 1;

}