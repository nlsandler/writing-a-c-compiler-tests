/* NOTE not supporting nested struct declarations */
struct inner {
    int x;
    int y;
};

struct outer {
    long l1;
    struct inner i;
    long l2;
};

int main() {
    struct outer foo = { 100, { 3, 4}, 10000000 };
    return foo.i.y + foo.l1 + (foo.l2 - 9999950);
}