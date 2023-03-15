int main(void) {
    int arr[2] = {1, 2};
    *arr = 3;
    *(arr + 1) = 4;
    return arr[0] + arr[1];
}