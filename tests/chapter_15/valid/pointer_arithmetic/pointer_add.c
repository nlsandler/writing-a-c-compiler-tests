/* Test pointer addition and subtraction to specify array indices
 * (but not subtracting two pointers to get the distance between them)*/

/* Addition */

// basic pointer addition test case
int add_constant_to_pointer(long *ptr, long expected) {
    ptr = ptr + 10;
    if ((*ptr) != expected) {
        return 1;
    }
    return 0;
}

// add negative index to pointer
int add_negative_index(unsigned *ptr, unsigned expected) {
    ptr = ptr + -10;
    if ((*ptr) != expected) {
        return 2;
    }
    return 0;    
}

// it doesn't matter whether we add pointer to int or vice versa
int add_pointer_to_int(int *ptr, int index, int expected) {
    int *ptr1 = ptr + index;
    int *ptr2 = index + ptr;
    if (ptr1 != ptr2) {
        return 3;
    }

    if (*ptr2 != expected) {
        return 4;
    }

    return 0;
}

// array index can be any integer type, not just int
int add_different_index_types(double *ptr, double expected) {
    double *ptr1 = ptr + 5;
    double *ptr2 = ptr + 5l;
    double *ptr3 = ptr + 5u;
    double *ptr4 = ptr + 5ul;

    if (ptr1 != ptr2) {
        return 5;
    }

    if (ptr1 != ptr3) {
        return 6;
    }

    if (ptr1 != ptr4) {
        return 7;
    }
    if (*ptr4 != expected) {
        return 8;
    }

    return 0;
}

// some helpers for following test case
int get_index(void) {
    static int index = 0;
    int result = index;
    index = index + 1;
    return result;
}

int *small_int_ptr; // in main, we'll make this point to 2, then -1

static int static_arr[4] = {5, 4, 3, 2};

int *get_ptr1(void) {
    return static_arr + 1;
}

int *get_ptr2(void) {
    return static_arr + 2;
}

// index and pointer can both be arbitrary expressions, not just constants and variables
int add_complex_expressions(int flag, int expected) {
    int *ptr = get_index() + (*small_int_ptr) + (flag ? get_ptr1() : get_ptr2());
    if (*ptr != expected)  {
        return 9;
    }
    return 0;
}

// add pointers to rows in a multi-dimensional array
int add_multi_dimensional(int (*nested)[3], int index, int expected) {
    int (*row_pointer)[3] = nested + index;
    if (**row_pointer != expected) {
        return 10;
    }
    return 0;
}

// add pointers to scalar elements in a multi-dimensional array
int add_multidimensional_sub(int (*nested)[3], int index, int expected) {
    int *row1 = *(nested + 1);
    int *elem_ptr = row1 + index;
    if (*elem_ptr != expected) {
        return 11;
    }

    return 0;
}

/* Subtraction */
int subtract_from_pointer(long *ptr, int index, int expected) {
    ptr = ptr - index;
    if (*ptr != expected) {
        return 12;
    }
    return 0;
}

// Subtract negative index from pointer
int subtract_negative_index(unsigned *ptr, unsigned expected) {
    ptr = ptr - -10;
    if ((*ptr) != expected) {
        return 13;
    }
    return 0;    
}

// array index can be any integer type, not just int
int subtract_different_index_types(double *ptr, double expected) {
    double *ptr1 = ptr - 5;
    double *ptr2 = ptr - 5l;
    double *ptr3 = ptr - 5u;
    double *ptr4 = ptr - 5ul;

    if (ptr1 != ptr2) {
        return 14;
    }

    if (ptr1 != ptr3) {
        return 15;
    }

    if (ptr1 != ptr4) {
        return 16;
    }
    if (*ptr4 != expected) {
        return 17;
    }

    return 0;
}

// index and pointer can both be arbitrary expressions, not just constants and variables
int subtract_complex_expressions(int flag, int expected) {
    int *ptr = (flag ? get_ptr1() : get_ptr2()) - (get_index() / 2);
    if (*ptr != expected)  {
        return 18;
    }
    return 0;
}


// subtract pointers to rows in a multi-dimensional array
int subtract_multi_dimensional(int (*nested)[3], int index, int expected) {
    int (*row_pointer)[3] = nested - index;
    if (**row_pointer != expected) {
        return 19;
    }

    return 0;
}

int main(void) {

    /* Addition test cases */

    long long_arr[12] = {0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 13};
    // long_arr[10] == 13
    int check = add_constant_to_pointer(long_arr, 13);
    if (check) {
        return check;
    }

    unsigned unsigned_arr[12] = {0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 42};
    unsigned *ptr_to_end = unsigned_arr + 12;
    // unsigned_arr[12 - 10] == 2
    check = add_negative_index(ptr_to_end, 2);
    if (check) {
        return check;
    }

    int int_arr[5] = {0, 98, 99};
    // int_arr[2] == 99
    check = add_pointer_to_int(int_arr, 2, 99);
    if (check) {
        return check;
    }

    double double_arr[11] = {0, 0, 0, 0, 0, 6.0};
    // double_arr[5] == 6.0
    check = add_different_index_types(double_arr, 6.0);
    if (check) {
        return check;
    }

    int x = 2;
    small_int_ptr = &x;
    // ptr = (1 ? get_ptr1() : get_ptr2())
    //    ==> &static_arr[1]
    // index = get_index() + (*small_int_ptr)
    //     ==> 0 + 2
    // static_arr[1 + 2] == 2
    check = add_complex_expressions(1, 2);
    if (check) {
        return check;
    }

    int nested_arr[3][3] = {{1, 2, 3}, {4, 5, 6}, {7,8,9}};
    // nested_arr[2][0] == 7
    check = add_multi_dimensional(nested_arr, 2, 7);
    if (check) {
        return check;
    }

    // nested_arr[1][2] == 6
    check = add_multidimensional_sub(nested_arr, 2, 6);
    if (check) {
        return check;
    }

    /* Subtraction test cases */
    // long_arr[4 - 2] == 3
    check = subtract_from_pointer(long_arr + 4, 2, 3);
    if (check) {
        return check;
    }

    // unsigned_arr[-(-10)] = 42
    check = subtract_negative_index(unsigned_arr, 42);
    if (check) {
        return check;
    }

    // double_arr[10 - 5] == 6.0
    check = subtract_different_index_types(double_arr + 10, 6.0);
    if (check) {
        return check;
    }

    x = -1;
    // pointer = (0 ? get_ptr1() : get_ptr2())
    //      ==> &static_arr[2]
    // index = get_index() + (*small_int_ptr)
    //     ==> 1 + -1
    // static_arr[2] == 3    
    check = subtract_complex_expressions(0, 3);
    if (check) {
        return check;
    }

    // nested_arr[2 - 1][0] == 4
    check = subtract_multi_dimensional(nested_arr + 2, 1, 4);
    if (check) {
        return check;
    }
    
    return 0;
}