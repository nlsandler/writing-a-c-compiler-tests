/* The same identifier can be used
 * in the same scope as both a function name and a label */
int foo() {
    goto foo;
    return 0;
    foo:
        return 1;
}

int main() {
    return foo();
}