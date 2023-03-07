double double_arr[2][2] = { {10.0, 9.0 }, {6.0, 7.0} };

int set_array_val() {
    double_arr[1][0] = 11.0;
    return 0;
}

int main() {
    set_array_val();
    return (double_arr[1][0] + double_arr[0][1] == 20.0);
}