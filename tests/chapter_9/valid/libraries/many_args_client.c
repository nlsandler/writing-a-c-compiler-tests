int fib(int a, int b);

int add_many_args(int a, int b, int c, int d, int e, int f, int g, int h);

int main(void) {
    int x = fib(3, 4);
    int y = add_many_args(x, 2, 3, 4, 5, 6, 7, 8);
    return x + y;
}