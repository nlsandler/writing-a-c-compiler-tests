int glob = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 0;

int client(int a, int b, int c, int d, int e, int f) {
    return a == 1 && b == 2 && c ==3 && d == 4 && e == 5 && f == 6;
}

int callee(void) {
    glob = glob + 1;
    glob2 = glob2 + 1;
    glob3 = glob3 + 1;
    // call client to make sure we clobber all caller-saved regs
    glob4 = client(1,2,3,4,5,6);
    return 0;
}

int target(void) {
    // make sure any variables that must be preserved across function calls are placed in callee-saved regs
    int a = 5 - glob;
    int b = glob2 * 2;
    int c = glob3 + 6;
    callee();
    return (a - glob == 2 && b - glob2 ==1 && c - glob3 == 5 && glob4 == 0);
}