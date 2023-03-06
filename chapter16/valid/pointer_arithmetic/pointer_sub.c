int main() {
    int arr[5] = { 5, 4, 3, 2, 1 };
    int *ptr4 = arr + 4;
    int *ptr2 = arr + 2;
    if (*ptr4 != 1) {
        return 0;
    }
    if (*ptr2 != 3) {
        return 0;
    }
    if (ptr4 - ptr2 != 2l) {
        return 0;
    }
    return 1;
}