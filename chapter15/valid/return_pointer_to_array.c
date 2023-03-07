int arr[3] = {0, 1, 2};

int (*foo())[3] {
    return &arr;
}

int main() {
    int (*array)[3] = foo();
    return array[0][1];
}