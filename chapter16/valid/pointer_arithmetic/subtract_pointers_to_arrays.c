int main() {
    int arr[3][3] = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };
    return &arr[2] - &arr[0];
}