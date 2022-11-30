int glob = 1;
int glob2 = 2;
int glob3 = 3;

int callee() {
    glob = glob + 1;
    glob2 = glob2 + 1;
    glob3 = glob3 + 1;
    return 0;
}

int target() {
    // make sure any variables that must be preserved across function calls are placed in callee-saved regs
    int a = 5 - glob;
    int b = glob2 * 2;
    int c = glob3 + 6;
    callee();
    return (a - glob == 2 && b - glob2 ==1 && c - glob3 == 5);
}