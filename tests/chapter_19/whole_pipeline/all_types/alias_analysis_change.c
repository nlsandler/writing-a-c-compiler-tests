#if defined SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wunused-parameter"
#endif

int foo(int *ptr) {
    return 2;
}

int target(void) {
    int x = 10;
    int *ptr = 0;
    if (0) {
        // need to update alias after dead code elim to recognize that
        // x is not actually aliased
        ptr = &x;
    }
    x = 5;     // this is a dead store
    foo(ptr);  // TODO could also validate that 0 is propagated to here as a
               // function argument
    return 0;
}

int main(void) {
    return target();
}