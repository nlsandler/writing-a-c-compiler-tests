int foo() {
    struct s {
        int a;
        int b;
    };
    struct s result = {1, 2};
    return result.a + result.b;
}

int main() {
    struct s blah = {foo(), foo()};
    return blah.a;
}