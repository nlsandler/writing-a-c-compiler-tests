long x = 1000;
long *arr[4] = {0, 0, 0, 0};

long *set_pointer() {
    arr[2] = &x;
    return arr[1];
}