struct main {
    int x;
    int y;
};

int main(void) {
    struct main x = { 1, 2};
    return x.x;
}