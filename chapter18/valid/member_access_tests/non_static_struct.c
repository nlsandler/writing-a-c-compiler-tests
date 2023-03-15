struct pair {
    int x;
    int y;
};

int foo(void) {
    struct pair p = { 9, 8 };
    p.y = p.y + 1;
    return p.y;
}

int main(void) {
    for (int i = 0; i < 10; i = i + 1) {
        foo();
    }
    return foo();
}