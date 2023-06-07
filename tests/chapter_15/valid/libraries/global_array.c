long x = 1000;
long *arr[4] = {0, 0, 0, 0};

long *set_pointer(void) {
    arr[2] = &x;
    return arr[1];
}