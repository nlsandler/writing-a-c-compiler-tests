struct pair {
    int *x;
    int y;
};

int main(void) {
    struct pair p = { 0, 7 };
    {
        struct pair { double x; double z; };
        struct pair foo;
        foo.x = p.x ? 1.0 : 2.0;
        return (int) foo.x;
    }
}