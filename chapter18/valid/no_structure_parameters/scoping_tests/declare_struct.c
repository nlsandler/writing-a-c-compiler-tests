int main(void) {
    struct pair {
        int x;
        double y;
    };
    struct pair p;
    p.x = 1;
    return p.x;
}