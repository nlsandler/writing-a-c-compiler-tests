int callee(int a, int b, int c, int d, int e, int f);

int target(int a, int b, int c, int d, int e, int f) {
    // make sure we coalesce all params into corresponding registers,
    // and result int EAX
    return callee(a,b,c,d,e,f);
}