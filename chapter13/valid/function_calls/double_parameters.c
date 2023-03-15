/* Test that we've properly implemented the calling convention for double parameters passed in registers */
int check_arguments(double a, double b, double c, double d, double e, double f, double g, double h);

int main(void) {
    return check_arguments(1.0, 2.0, 3.0, 4.0, -1.0, -2.0, -3.0, -4.0);
}

int check_arguments(double a, double b, double c, double d, double e, double f, double g, double h) {
    return a == 1.0 && b == 2.0 && c == 3.0 && d == 4.0
        && e == -1.0 && f == -2.0 && g == -3.0 && h == -4.0;
}