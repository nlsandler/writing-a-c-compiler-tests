int main(void) {
    int idx = 3;
    int arr[3] = {1, 2, 3};
    int ret = arr[idx = 1];
    return ret + idx;
}