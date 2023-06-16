/* Test initializing nested arrays with automatic storage duration */
int simple(void) {
    int arr[3][3] = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };
    for (int i = 0; i < 3; i = i + 1) {
        for (int j = 0; j < 3; j = j + 1) {
            if (arr[i][j] != i * 3 + j + 1) {
                return 42;
            }
        }        
    }

    return 0;
}

int partial(void) {
    /* if an array is partially initialized, any elements that aren't
     * explicitly initialized (including nested arrays) should be zeroed out.
     */


    int arr[3][2][5] = {
        {{1, 2},
         {3, 4, 5}},
        {{6}},
        {{7},
         {8, 9, 10, 11, 12}}};
    
    // this spaghetti code just checks the value of each array element
    int next_expected = 1;    
    for (int i = 0; i < 3; i = i + 1) {
        for (int j = 0; j < 2; j = j + 1) {
            for (int k = 0; k < 5; k = k + 1) {
                int val = arr[i][j][k];                
                int is_initialized = 0;
                if (i == 0) {
                    if (k < 2) {
                        // in both columns of arr[0], elements 0 and 1 are initialized
                        is_initialized = 1;
                    } else if (j == 1 && k < 3) {
                        // in arr[0][1], element 2 is also initizlied
                        is_initialized = 1;
                    }
                } else if (j == 0 && k == 0) {
                    // arr[i][0][0] initialized in every row
                    is_initialized = 1;
                } else if (i == 2 && j == 1) {
                    // all elements in arr[2][1] are initialized
                    is_initialized = 1;
                }

                if (is_initialized) {
                    if (val != next_expected) {
                        return (i * 10 + j * 5 + k) + 1;
                    }
                    next_expected = next_expected + 1;
                } else {
                    if (val) {
                        // this element wasn't explicitly initialized, so should be 0!
                        return (i * 10 + j * 5 + k) + 1;
                    }
                }
            }
        }
    }

    return 0;
}

unsigned int three(void) {
    return 3u;
}

int non_constant_and_type_conversion(long arg1, int *ptr) {
    /* elements in a compound initializer may include non-constant expressions
     * and expressions of other types, which are converted to the right type
     * as if by assignment */

    // arg1 should be 2000, ptr should point to -4
    double arr[3][2] = {
        { arg1, arg1 / *ptr },
        { three() }
    };

    if (arr[0][0] != 2000.0) {
        return 50;
    }

    if (arr[0][1] != -500.0) {
        return 51;
    }

    if (arr[1][0] != 3.0) {
        return 52;
    }

    if (arr[1][1] || arr[2][0] || arr[2][1]) {
        return 53;
    }

    return 0;
}

long one = 1l;
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
    int arr[3][1] = { {one * 2l}, {one + three()} };
    unsigned int u = 2684366905;

    if (i != -1) {
        return 54;
    }

    if ( arr[0][0]!= 2) {
        return 55;
    }

    if (arr[1][0] != 4) {
        return 56;
    }

    if (arr[2][0]) {
        return 57;
    }

    if (u != 2684366905) {
        return 58;
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

    int x = -4;
    check = non_constant_and_type_conversion(2000, &x);
    if (check) {
        return check;
    }

    check = preserve_stack();
    if (check) {
        return check;
    }
    return 0;
}

