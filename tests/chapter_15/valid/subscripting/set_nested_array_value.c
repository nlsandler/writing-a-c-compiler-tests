int main(void) {
    int arr[3][2] = { {1, 4}, {2, 3}, {5, 7} };
    arr[2][1] = 5;
    return arr[2][1] - arr[1][1];
}