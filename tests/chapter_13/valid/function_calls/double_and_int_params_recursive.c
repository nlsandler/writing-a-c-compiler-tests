/* A recursive function in which both double and integer parameters
 * are passed in registers and on the stack */
double fun(int a, double m, int b, double n, int c, double o,
        int d, double p, int e, double q, int f, double r,
        int g, double s, int h, double t, int i, double u) {
    if (a + b + c + d + e + f + g + h + i <= 0) {
        if (m + n + o + p + q <= 0.0) {
            return s + t + u;
        } else {
            return fun(a, m - 1.0, b, n, c, o, d, p, e, q, f, r, g, s + 1.0, h, t, i, u);
        }
    } else {
        return fun(a, m, b - 1, n, c, o, d, p, e, q, f, r, g, s, h, t, i, u);
    }
}

int main(void) {
    double d = fun(1, 2.0, 3, 4.0, 5, 6.0, 7, 8.0, 9, 10.0, 11, 12.0, 13, 14.0, 15, 16.0, 17, 18.0);
    return (d == 78.00);
}