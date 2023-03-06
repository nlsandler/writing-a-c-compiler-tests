int main()
{
    long arr[4] = {4, 5, 6, 7};
    long *ptr = arr;
    long(*arr_ptr)[4] = (long(*)[4])ptr;
    return arr_ptr == &arr;
}