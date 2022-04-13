int main() {
    /* Nested function definitions are not permitted */
    int foo() {
        return 1;
    }
    return foo();
}