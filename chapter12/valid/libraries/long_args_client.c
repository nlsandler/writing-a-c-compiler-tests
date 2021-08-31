/* This is identical to the test case in tests/chapter12/valid/long_expressions/long_args.c,
 * but split across multiple files.
 */

int test_sum(long a, long b, int c, int d, int e, int f, int g, int h, long i);

int main() {
    return test_sum(34359738368l, 34359738368l, 0, 0, 0, 0, 0, 0, 34359738368l);
}