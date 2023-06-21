#if defined SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wdiv-by-zero"
#endif

int callee(void) {
    return 1 / 0;
}

int target(void) {
    // when we enable unreachable code elimination and constant folding,
    // call to callee() shoudl be optimized away, initialized assignmnet (i = 10
    // should not)
    int i = 0;
    for (i = 10; 0; i = i * 100) callee();
    return i;
}

int main(void) {
    return target();
}