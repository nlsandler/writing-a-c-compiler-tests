int foo(int idx, int v) {
    static int arr[3];
    arr[idx] = v;
    return arr[1];
}

int main() {
    foo(1, 8);
    foo(2, 9);
    return foo(3, 10);
}