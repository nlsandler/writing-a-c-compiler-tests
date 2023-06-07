int foo(int p) {
    static int arr[3] = { p, p + 1, 0};
    return arr[2];
}

int main(void) {
    return foo(5);
}