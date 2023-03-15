int main(void) {
    int arr[3][3] = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };
    int (*row)[3] = &arr[2] - 1;
    return row[0][0];

}