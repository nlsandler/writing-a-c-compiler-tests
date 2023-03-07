struct inner {
    int a;
    int b;
};

struct outer {
    char c;
    struct inner i;
};

struct outer o;

int main() {
    struct inner i = {7, 8};
    o.c = 1;
    o.i = i;
    return o.i.b;
}