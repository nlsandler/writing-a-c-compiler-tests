int fib(int a);

int multiply_many_args(int a, int b, int c, int d, int e, int f, int g, int h);

int main(void) {
    int x = fib(4);
    int y = multiply_many_args(x, 2, 3, 4, 5, 6, 7, 8);
    if (x != 3) {
        return 1;
    }
    if (y != 589680) {
        return 2;
    }
    return x + (y % 256);
}