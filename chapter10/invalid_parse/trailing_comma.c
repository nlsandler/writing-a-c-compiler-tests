int foo(int a, int b, int c) {
    return a + b + c;
}

int main() {
    /* Trailing commas aren't permitted in argument lists */
    return foo(1, 2, 3,);
}