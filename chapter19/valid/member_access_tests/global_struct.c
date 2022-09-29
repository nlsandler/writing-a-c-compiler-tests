struct pair { double x; double y; };
static struct pair foo;

void set_foo(double a, double b) {
    foo.x = a;
    foo.y = b;
}

int main() {
    set_foo(8.0, 7.0);
    return foo.y;
}