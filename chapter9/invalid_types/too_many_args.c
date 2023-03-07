int foo(int a) {
    return a + 1;
}

int main() {
    /* foo is called with too many arguments */
    return foo(1, 2);
}