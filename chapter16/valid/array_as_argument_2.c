int foo(int a[5]) {
    a[4] = 0;
    return 0;
}

int main() {
    int arr[5] = {8, 7, 6, 5, 4};
    foo(arr);
    return arr[4];
}