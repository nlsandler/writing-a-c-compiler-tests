int foo(int a, int b, int c) {
    int arr[3] = {a, b, c};
    return arr[0] + arr[1] + arr[2];
}

int main(void) {
    return foo(5, 6, 7);
}