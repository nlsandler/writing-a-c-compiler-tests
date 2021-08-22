/* This declares a global variable */
extern int foo;

int main() {
    /* Treating a variable as a function is a type error. */
    return foo();
}