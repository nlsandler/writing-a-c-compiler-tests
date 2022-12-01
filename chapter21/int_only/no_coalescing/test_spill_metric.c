int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;

int callee(int a, int b, int c, int d, int e);
int check_globals();

int target(int a, int b, int c, int d, int e, int flag) {
    // make sure we spill nodes with lower spill costs first
    int f = glob1;

    // put uses of these variables in branches to avoid copy prop
    if (flag) {
        a = a + 1;
        b = b - 2;
        c = c * 3;
        d = d / 4;
        e = e % 5;
    } else {
        a = a - 1;
        b = b + 2;
        c = c / 3;
        d = d * 4;
        e = e * e;
    }


    int result = callee(a, b, c, d, e);
    // TODO: wrapper needs to validate these
    glob1 = a;
    glob2 = b;
    glob3 = c;
    glob4 = d;
    glob5 = e + result;
    check_globals();
    return f;
}