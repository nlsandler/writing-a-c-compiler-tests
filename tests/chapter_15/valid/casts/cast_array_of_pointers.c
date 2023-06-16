/* Test that we can convert between different pointer types, including pointers to arrays */

int main(void)
{
    int simple_array[2] = {1, 2};
    // Array of pointers to arrays
    int(*ptr_arr[3])[2] = {&simple_array, 0, &simple_array};
    // Cast from one pointer type to another
    // Note: dereferencing other_ptr would violate strict aliasing,
    // but casting/comparing it is okay.
    long *other_ptr = (long *)ptr_arr;
    // After round-trip cast from int(**)[2] to long * and back,
    // this must compare equal to its original value.
    return (int(**)[2])other_ptr == ptr_arr;
}