/* Make sure we can implicity convert null pointer constants to pointer type */

// convert static variable initializer
double *d = 0l;

int expect_null_param(int *val) {
    // validate that this is a null pointer
    return (val == 0u);
}

long *return_null_ptr() {
    return 0; // convert return value to pointer
}

int main() {
    int x = 10;
    int *ptr = &x;
    
    // convert to pointer for assignment
    ptr = 0ul;

    // convert function argument to pointer
    if (!expect_null_param(0))
        return 0;

    long *null_ptr = return_null_ptr();
    if (null_ptr != 0)
        return 0;

    // convert ternary operand to null pointer
    ptr = &x;
    int *ternary_result = 10 ? 0 : ptr;
    return !ternary_result;
}