int main(void) {
    int *arr[3];
    int a = 4;
    int b = 5;
    int c = 6;
    arr[0] = &a;
    arr[1] = &b;
    arr[2] = &c;
    *arr[1] = 9;
    return b;
}