/* This test case is identical to chapter14/valid/function_calls/double_and_int_params_recursive.c
 * but split across two files */
double fun(int a, double m, int b, double n, int c, double o,
        int d, double p, int e, double q, int f, double r,
        int g, double s, int h, double t, int i, double u);

int main() {
    double d = fun(1, 2.0, 3, 4.0, 5, 6.0, 7, 8.0, 9, 10.0, 11, 12.0, 13, 14.0, 15, 16.0, 17, 18.0);
    return (d == 78.00);
}