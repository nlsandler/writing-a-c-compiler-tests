extern void x;

void foo() {
    return;
}

int main() {
    // the standard is ambiguous on whether you can declare a void variable,
    // but you definitely can't assign to it
    x = foo();
    return 0;
}