int main(void) {
    int arr[6] = { 1, 2, 3, 4, 5, 6 };
    int *arr_elem = arr + 2;
    return *arr_elem == arr[2];
}