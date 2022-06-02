int foo(int a, int b, int c) {
    int arr[3] = { a, a, b };
    return arr[2] + c;
}

int main() {
    return foo(1, 2, 3);
}