struct pair {
    int x;
    int y;
};

int foo(struct pair p);

int main(void) {
    struct pair arg = {1, 2};
    return foo(arg);
}