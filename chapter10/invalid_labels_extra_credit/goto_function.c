int foo() {
    return 3;
}

int main() {
    /* You can't use a function name as a goto label */
    goto foo;
    return 3;
}