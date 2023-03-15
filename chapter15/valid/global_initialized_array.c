double double_arr[3] = {1.0, 2.0, 3.0};

int foo(void) {
    for (int i = 0; i < 3; i = i + 1) {
        double_arr[i] = double_arr[i] * 2.0;
    }
    return 0;
}

int main(void) {
    foo();
    return (double_arr[2] == 3.0 * 2.0);
}