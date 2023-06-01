struct inner { 
    double a;
    char b;
};

struct outer {
    struct inner foo;
    int bar;
};

int main(void) {
    struct outer s;
    s.foo.a = 1.0;
    s.foo.b = 2;
    s.bar = 10;
    struct inner i = s.foo;
    i.a = 5.0;
    return s.foo.a + i.a + s.bar;
}