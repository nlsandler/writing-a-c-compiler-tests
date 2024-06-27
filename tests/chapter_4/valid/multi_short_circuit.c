#ifdef SUPPRESS_WARNINGS
#ifndef __clang__
#pragma GCC diagnostic ignored "-Wparentheses"
#endif
#endif
int main(void) {
    return 0 || 0 && (1 / 0);
}