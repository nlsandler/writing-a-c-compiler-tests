int main() {
    int arr[3] = {1, 2, 3};
    int (*ptr_to_arr)[3] = &arr;
    return (*ptr_to_arr)[1];
}