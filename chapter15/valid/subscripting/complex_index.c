long foo(long *arr, int *a, int b) {
    return arr[a[b]];
}

int main(void) {
    long arr[3] = { 5l, 6l, 7l };
    int indices[3] = { 9, 5, 1};;
    long res = foo(arr, indices, 2);
    return (res == 6l);
}