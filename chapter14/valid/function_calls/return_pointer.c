/* Test returning a pointer from a function */
int *return_pointer(int *in) {
    return in;
}

int main(void) {
    int x = 10;
    int *x_ptr = return_pointer(&x);

    if (*x_ptr != 10)
        return 0;

    x = 100;
    if (*x_ptr != 100)
        return 0;

    if (x_ptr != &x)
        return 0;

    return 1;
}