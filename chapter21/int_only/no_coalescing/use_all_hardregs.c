int glob = 20;

int client(int a, int b, int c, int d, int e, int f, int g) {
    return a ==1 && b == 2 && c == 3 && d == 4 && e == 5 && f == 6 && g== 400;
}

int target(int a, int b, int c, int d, int e, int f) {
    // this uses all hardregs (we don't need to save/spill callee-saved regs)
    int tmp = glob * glob;
    return client(a, b, c, d, e, f, tmp);
}