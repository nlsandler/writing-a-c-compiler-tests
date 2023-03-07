double double_arr[8];

int foo() {
    for (int i = 0; i < 8; i = i + 1) {
        double_arr[i] = double_arr[i] * 2.0;
    }
    return 0;
}

int main() {
    double c = 3.1;
    double_arr[5] = c;
    foo();
    return (double_arr[5] == c * 2.0);
}