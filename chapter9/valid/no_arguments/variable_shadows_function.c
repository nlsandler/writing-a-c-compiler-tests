int main() {
    int foo();

    int x = foo();
    if (x > 0) {
        int foo  = 3;
        x = x + foo;
    }
    return x;
}

int foo() {
    return 4;
}