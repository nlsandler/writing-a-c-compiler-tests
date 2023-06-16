/* Test initialzing one-dimensional arrays with automatic storage duration */

int simple(void) {

    // Initialize array with three constants
    unsigned long arr[3] = {18446744073709551615UL, 9223372036854775807UL, 100ul};
    if (arr[0] != 18446744073709551615UL) {
        return 1;
    }

    if (arr[1] != 9223372036854775807UL) {
        return 2;
    }

    if (arr[2] != 100ul) {
        return 3;
    }

    return 0;
}

int partial(void) {
    /* if an array is partially initialized, any elements that aren't
     * explicitly initialized should be zero.
     */
    double arr[5] = {1.0, 123e4};

    if (arr[0] != 1.0) {
        return 4;
    }

    if (arr[1] != 123e4) {
        return 5;
    }

    // remaining elements should be 0
    if (arr[2] || arr[3] || arr[4]) {
        return 6;
    }

    return 0;
}

// simple function we can use in the test case below
int three(void) {
    return 3;
}

int non_constant(long arg1, int *ptr) {
    /* An initializer can include non-constant expressions, including function parameters */

    // arg1 should be -68719476736l, ptr should point to an int
    long var = arg1 * three();
    long arr[5] = { arg1,
                    three() * 7l,
                    - (long) *ptr,
                    var + (arg1 ? 2 : 3) }; // fifth element  not initialized, should be 0
    if (arr[0] != -68719476736l) {
        return 7;
    }
    if (arr[1] != 21l) {
        return 8;
    }
    if (arr[2] != -1l) {
        return 9;
    }
    if (arr[3] != -206158430206l){
        return 10;
    }
    if (arr[4] != 0l) {
        return 11;
    }
    return 0;
    
}

long one = 1l;

int type_conversion(int *ptr) {
    /* elements in a compound initializer are converted to the right type as if by assignment */
    // ptr should point to -100
    unsigned long arr[4] = { 3458764513821589504.0, // convert double to ulong
                            *ptr, // dereference to get int, then convert to ulong - end up with 2^64 - 100
                            // truncate ulong_max to unsigned int, then back to ulong - will end up with UINT_MAX
                            (unsigned int) 18446744073709551615UL,
                            -one // converts to ULONG_MAX
                            };
    
    if (arr[0] != 3458764513821589504ul) {
        return 12;
    }

    if (arr[1] != 18446744073709551516ul) {
        return 13;
    }

    if (arr[2] != 4294967295U) {
        return 14;
    }

    if (arr[3] != 18446744073709551615UL) {
        return 15;
    }

    return 0;
}

int preserve_stack(void) {
    /* Initializing an array must not corrupt other objects on the stack. */
    int i = -1;

    /* Initialize with expressions of long type - make sure they're truncated
     * before being copied into the array.
     * Also use an array of < 16 bytes so it's not 16-byte aligned, so there are
     * eightbytes that include both array elements and other values.
     * Also leave last element uninitialized; in assembly, we should set it to zero without
     * overwriting what follows
     */
    int arr[3] = {one * 2l, one + three() };
    unsigned int u = 2684366905;

    if (i != -1) {
        return 16;
    }

    if ( arr[0]!= 2) {
        return 17;
    }

    if (arr[1] != 4) {
        return 18;
    }

    if (arr[2]) {
        return 19;
    }

    if (u != 2684366905) {
        return 20;
    }

    return 0;
}


int main(void) {

    int check = simple();
    if (check) {
        return check;
    }

    check = partial();
    if (check) {
        return check;
    }

    int a = 1;
    check = non_constant(-68719476736l, &a);
    if (check) {
        return check;
    }
    a = -100;
    check = type_conversion(&a);
    if (check) {
        return check;
    }
    check = preserve_stack();
    if (check) {
        return check;
    }

    return 0;
}