#if defined SUPPRESS_WARNINGS && !defined __clang__
#pragma GCC diagnostic ignored "-Wempty-body"
#endif

int target(void) {
    // if we enable DSE and dead code elim, x should go away
    int x = 10;
    if (x)
        ;
    return 10;
}

int main(void) {
    return target();
}