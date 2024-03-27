#ifdef SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wparentheses"
#endif

int main(void) {
    return 2 >> 5 || 3 & 6 == 3 << 1;
}