/* Helper functions defined in tests/chapter_20/libraries/util.c */

/* The validate_* functions return 0 on success,
 * print and exit with code -1 on failure.
 */

int check_one_int(int actual, int expected);

// Validates a == start, b == start + 1, ...e == start + 5
int check_5_ints(int a, int b, int c, int d, int e, int start);

// Validates a == start, b == start + 1, ... l == start + 11
int check_12_ints(int a, int b, int c, int d, int e, int f, int g, int h, int i,
                  int j, int k, int l, int start);

// return x; used to get constants in a way that can't be optimized away
int id(int x);

// Validates a == start, b == start + 1, ..., *k == start + 10, *l == start + 11
int check_12_vals(int a, int b, int c, int d, int e, int f, int g, int h, int i,
                  int j, long *k, double *l, int start);


// validates a == start, b == start + 1, ... n == start + 13
// and exits early if they don't have those values
// NOTE: assumes a-n are small integral values that can be represented exactly
// as double so no rounding error
int check_14_doubles(double a, double b, double c, double d, double e,
                           double f, double g, double h, double i, double j,
                           double k, double l, double m, double n,
                           double start);