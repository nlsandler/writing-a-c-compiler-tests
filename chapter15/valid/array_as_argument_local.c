int main(void) {
    int foo(int a[5]);
    int arr[5] = {8, 7, 6, 5, 4};
    return foo(arr);
}

int foo(int a[4]) {
    return a[3];
}