int foo() {
    label:
        return 0;
}

int main() {
    /* You can't goto a label in another function */
    goto label;
    return 1;
}