struct s {
    char arr[3];
    double d;
    int arr2[2];
    char arr3[5];
};

int main(void) {
    struct s first = { { 1, 2, 3 },
                        12.0, {4, 5},
                        { 6, 7, 8, 9, 10} };
    struct s second = first;
    for (int i = 0; i < 3; i = i + 1) {
        if (second.arr[i] != i + 1)
            return 0;
    }
    if (second.arr2[0] != 4 || second.arr2[1] != 5)
        return 0;
    for (int i = 0; i < 3; i = i + 1) {
        if (second.arr3[i] != i + 6)
            return 0;
    }
    return second.d == 12.0;
}