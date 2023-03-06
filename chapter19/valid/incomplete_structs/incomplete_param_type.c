struct s;

int foo(struct s blah);

struct s {
    int a;
    int b;
};

int main() {
    struct s arg = { 1, 2};
    return foo(arg);
}

int foo(struct s blah) {
    return blah.a + blah.b;
}