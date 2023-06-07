int main(void) {
    int arr[2] = {1, 2};
    // dereferenced expressions, including dereferenced results of
    // pointer arithmetic, are valid lvalues
    *arr = 3;
    *(arr + 1) = 4;
    return arr[0] + arr[1];
}