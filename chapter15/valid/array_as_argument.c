int foo(int a[5]) {
    return a[3];
}

int main() {
    int arr[5] = {8, 7, 6, 5, 4};
    return foo(arr);
}