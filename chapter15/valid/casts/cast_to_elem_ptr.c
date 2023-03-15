int main(void)
{
    int arr[3] = {1, 2, 3};
    int(*arr_ptr)[3] = &arr;
    // cast pointer to array to pointer to first element
    int *ptr = (int *)arr_ptr;
    return *ptr;
}