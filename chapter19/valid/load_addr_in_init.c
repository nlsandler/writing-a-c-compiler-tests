struct pair {
    int x;
    int *y;
};

int main() {
    struct pair p = { 3, &(p.x) };
    return p.x + *p.y;
}