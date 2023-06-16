/* Declare the same global array multiple times w/ equivalent declarators */

// an array of four longs
long int(arr)[4] = {1, 2, 3, 4};

int long arr[4ul];

// a pointer to a two-dimensional array
int (*ptr_to_arr)[3][6l];

int((*(ptr_to_arr))[3l])[6u] = 0;

// an array of pointers
int *array_of_pointers[3] = {0, 0, 0};

int validate_arr(void) {
    for (int i = 0; i < 4; i = i + 1) {
        if (arr[i] != i + 1) {
            return i + 1;
        }
    }
    return 0;
}

int validate_ptr_to_arr(void) {
    // at first ptr_to_arr should be null
    if (ptr_to_arr) {
        return 5;
    }

    static int nested_arr[3][6];
    ptr_to_arr = &nested_arr;
    ptr_to_arr[0][2][4] = 100;
    if (nested_arr[2][4] != 100) {
        return 6;
    }
    return 0;
}

int validate_array_of_pointers(int *ptr) {

    extern int *((array_of_pointers)[3]); // make sure we can redeclare this locally

    // make sure every array element is null
    // then assign ptr to each of them
    for (int i = 0; i < 3; i = i + 1) {
        if (array_of_pointers[i])
            return 7;
        array_of_pointers[i] = ptr;
    }

    // update value through pointer
    array_of_pointers[2][0] = 11;

    if (*ptr != 11) {
        return 8;
    }

    for (int i = 0; i < 3; i = i + 1) {
        if (array_of_pointers[i][0] != 11) {
            return 9;
        }
    }
    return 0;

}

int main(void)
{
    // make sure arr has the right type/initial values;
    int check = validate_arr();
    if (check) {
        return check;
    }

    // make sure ptr_to_arr has right type
    check = validate_ptr_to_arr();
    if (check) {
        return check;
    }

    // make sure array_of_pointers has the right type
    int x = 0;
    check = validate_array_of_pointers(&x);
    if (check) {
        return check;
    }

    return 0;
}