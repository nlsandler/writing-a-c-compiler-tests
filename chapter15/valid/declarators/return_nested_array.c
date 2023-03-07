int arr[3] = {1, 1, 1};

int (*foo(int x, int y))[3] {
    return &arr;
}

int main() {
    int (*arr)[3] = foo(2, 3);
    return (*arr)[1];
}