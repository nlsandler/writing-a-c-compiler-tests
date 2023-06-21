#ifdef SUPPRESS_WARNINGS
#ifndef __clang__
#pragma GCC diagnostic ignored "-Wswitch-unreachable"
#endif
#endif

int main(void) {
    int a = 3;
    int b = 0;
    switch(a) {
        int a = 0;
    case 3:
        a = 4;
        b = a;
    }
    return a + b;
}