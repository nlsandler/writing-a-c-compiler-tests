/* The same label can be used in multiple functions */
int foo() {
    goto label;
    return 0;
    label:
        return 5;
}

int main() {
    goto label;
    return 0;
    label:
        return foo();
}