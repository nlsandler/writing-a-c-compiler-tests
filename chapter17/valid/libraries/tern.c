void* calloc( unsigned long num, unsigned long size );

int foo(int flag, double *d, int **arr) {
    void *buff = flag ? d : (void *) arr;
    if (flag) {
        return ((double *) buff)[2];
    } else {
        return ((int **) buff)[1][0];
    }
}
