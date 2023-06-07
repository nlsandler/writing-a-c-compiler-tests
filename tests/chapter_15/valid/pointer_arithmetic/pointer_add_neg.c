int main(void) {
    int arr[3] = {1, 2, 3};
    int *ptr = arr + 2;
    int *ptr2 = -1 + ptr;
    return *ptr2;
}