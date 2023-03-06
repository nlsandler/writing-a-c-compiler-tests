struct small_alignment {
    int a;
    int b;
    char c;
};

int main() {

    struct small_alignment arr[3] = { {0, 1, 2}, {3, 4, 5}, {6, 7, 8}};
    struct small_alignment new = {9, 9, 9};
    arr[1] = new;
    if (arr[0].a == 0 && arr[0].b == 1 && arr[0].c == 2
        && arr[1].a == 9 && arr[1].b == 9 && arr[1].c == 9
        && arr[2].a == 6 && arr[2].b == 7 && arr[2].c == 8)
        return 1;
    return 0;

}