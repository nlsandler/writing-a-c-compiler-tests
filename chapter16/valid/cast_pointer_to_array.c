int main() {
    int nested[2][2] = {{1, 2} , {3, 4}};
    int (*arr_pointer)[2][2] = &nested;
    int (*cast_array_pointer)[4] = (int (*)[4]) arr_pointer;
    return (*cast_array_pointer)[3];
}