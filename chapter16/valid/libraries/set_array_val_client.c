int set_nth_element(double *arr, int idx);

int main() {
    double arr[5] = {0.0, 0.0, 0.0, 0.0, 0.0};
    set_nth_element(arr, 4);
    for (int i = 0; i < 4; i = i + 1) {
        if (arr[i] != 0) {
            return 0;
        }
    }
    if (arr[4] == 8)
        return 1;
    return 0;
}