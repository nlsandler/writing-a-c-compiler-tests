int main(void) {
    int arr[4] = {1, 2, 3, 4};
    int *ptr = (int *) arr;
    ptr = ptr + 1;
    return ptr[2];
}