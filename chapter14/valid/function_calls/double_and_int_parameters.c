/* Test that we've properly implemented the calling convention for passing doubles and ints in registers */
int check_arguments(double d1, double d2, int i1, double d3, double d4, int i2, int i3,
                    int i4, double d5, double d6, double d7, int i5, double d8) {
    return d1 == 1.0 && d2 == 2.0 && d3 == 3.0 && d4 == 4.0 && d5 == 5.0
        && d6 == 6.0 && d7 == 7.0 && d8 == 8.0 && i1 == 101 && i2 == 102 && i3 == 103
        && i4 == 104 && i5 == 105;
}

int main() {
    return check_arguments(1.0, 2.0, 101, 3.0, 4.0, 102, 103, 104, 5.0, 6.0, 7.0, 105, 8.0);
}