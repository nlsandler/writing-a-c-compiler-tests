int main()
{
    int simple_array[2] = {1, 2};
    int(*ptr_arr[3])[2] = {&simple_array, 0, &simple_array};
    // cast from one pointer type to another
    long *other_ptr = (long *)ptr_arr;
    return (int(**)[2])other_ptr == ptr_arr;
}