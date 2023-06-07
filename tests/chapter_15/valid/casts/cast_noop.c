int main(void) {
    int arr[4] = {1, 2, 3, 4};
    // this cast is a no-op since arr is implicitly converted
    // to a pointer to its first element anyway
    int *ptr = (int *) arr;
    ptr = ptr + 1;
    return ptr[2];
}