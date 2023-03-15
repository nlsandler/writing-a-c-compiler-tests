struct s {
    char arr[12];
    double d;
};

int main(void) {
    struct s first = { { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 12.0};
    struct s second = first;
    for (int i = 0; i < 12; i = i + 1) {
        if (second.arr[i] != i + 1)
            return 0;
    }
    return second.d == 12.0;
}