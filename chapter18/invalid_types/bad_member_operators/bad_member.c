struct s {
    int x;
    int y;
};

int main(void) {
    struct s foo = {1, 2};
    return foo.blah;
}