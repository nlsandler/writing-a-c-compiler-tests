int main(void) {
    int arr[3] = { 1, 2, 3};
    int (*ptr_to_array)[3] = 0;
    *ptr_to_array = arr;
}