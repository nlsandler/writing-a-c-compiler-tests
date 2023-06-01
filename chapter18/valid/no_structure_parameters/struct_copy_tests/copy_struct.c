struct pair {
    int x;
    int y;
};

int main(void) {
    struct pair p1 = {1, 2};
    struct pair p2 = {0, 0};
    p2 = p1;
    p2.x = 4;
    return p1.x + p2.x + p2.y;
}