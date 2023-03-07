struct pair {
    int x;
    double y;
};

double foo(struct pair p) {
    return p.y;
}

int main() {
    struct pair x = { 1, 2.0 };
    return foo(x) == 2.0;
}