#include <signal.h>

extern int glob1;
extern int glob2;
extern int glob3;
extern int glob4;
extern int glob5;

int callee(int a, int b, int c, int d, int e) {
    if (a == 2 && b == 0 && c == 9 && d == 1 && e == 0)
        return 1;
    
    return -100;
}

int check_globals(void) {
    if (glob1 == 2 && glob2 == 0 && glob3 == 9 && glob4 == 1 && glob5 == 1)
        return 0;
    raise(SIGSEGV);
    return 0;
}