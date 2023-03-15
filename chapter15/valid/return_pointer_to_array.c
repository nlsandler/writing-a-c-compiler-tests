int arr[3] = {0, 1, 2};

int (*foo(void))[3] {
    return &arr;
}

int main(void) {
    int (*array)[3] = foo();
    return array[0][1];
}