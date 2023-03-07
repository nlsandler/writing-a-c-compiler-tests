int *foo(int arr[3]) {
    return arr + 1;
}

int main() {
    int arr[3] = {4, 5, 6};
    int *arr_incr = foo(arr);
    return arr_incr[0];
}