void* calloc( unsigned long nmemb, unsigned long size );

int foo(int flag, double *d, int **arr);

int main(void) {
    int x = 0;
    int y = 1;
    int z = 2;
    double arr[3] = {1.0, 2.0, 3.0};
    int *ptr_arr[3] = { &x, &y, &z };
    int a = foo(0, arr, ptr_arr);
    int b = foo(1, arr, ptr_arr);
    return a + b;
}