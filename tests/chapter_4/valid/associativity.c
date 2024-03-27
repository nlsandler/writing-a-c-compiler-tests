#ifdef SUPPRESS_WARNINGS
#ifndef __clang__
#pragma GCC diagnostic ignored "-Wparentheses"
#endif
#endif

int main(void) {
    return 5 >= 0 > 1 <= 0;
}