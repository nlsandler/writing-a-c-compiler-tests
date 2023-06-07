struct pair {
    int x;
    int *y;
};

int main(void) {
    struct pair p = { 3, &(p.x) };
    return p.x + *p.y;
}