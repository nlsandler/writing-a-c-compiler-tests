int foo(int (*ptr_to_array)[3]) {
    return ptr_to_array[0][1];
}

int main(void) {
    int arr[3] = { 10, 11, 12};
    return foo(&arr);
}