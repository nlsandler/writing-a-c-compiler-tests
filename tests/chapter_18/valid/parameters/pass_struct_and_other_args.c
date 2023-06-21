#ifdef SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wunused-parameter"
#endif

struct pair {
    int x;
    double y;
};

double foo(struct pair p, int a, int b, int c, int d, int e, int f, int g) {
    return p.y + g;
}

int main(void) {
    struct pair x = { 1, 2.0 };
    return foo(x, 0, 0, 0, 0, 0, 0, 1) == 3.0;
}