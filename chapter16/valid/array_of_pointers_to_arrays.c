int main() {
    int x = 0;
    int y = 1;
    int z = 2;
    int *arr[3] = { &x, &y, &z };
    int *arr2[3] = {&z, &y, &x};
    // an array of pointers to arrays of pointers
    int *(*array_of_pointers[3])[3] = {&arr, &arr2, &arr};
    return *(array_of_pointers[1][0][1]) + (*array_of_pointers[2])[2][0];
}