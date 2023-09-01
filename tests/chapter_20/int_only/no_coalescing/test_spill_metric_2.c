int callee(int ok);

int glob1 = 32;
int glob2 = 2;
int glob3 = 3;
int glob4 = 9;
int glob5 = 5;
int glob6 = 16;

// when multiple pseudos have the same spill cost, make sure we spill the one with the highest degree
int target(void) {

    // to_spill and a-e form a clique and must go in callee-saved regs
    int to_spill = glob1;
    int a = glob2;
    int b = glob3;
    int c = glob4;
    int d = glob5;
    int e = glob6;

    callee(1);

    int ok = 1;
    if (!(a == glob2 + 2 && b == glob3 -2 && c == glob4 * 3 && d == glob5 - 5 && e == glob6 * 2))
        ok = 0; // set ok instead of just returning b/c return increases spill cost of callee-saved tmps

    // to_spill and f-j form a clique and must go in callee-saved regs
    int f = glob2;
    int g = glob3;
    int h = glob4;
    int i = glob5;
    int j = glob6;
    // return 'ok' as result (so we can validate that a/b/etc had expected values)
    // also update global vars
    int result = callee(ok);
    if (!(f == glob2 + 2 && g == glob3 -2 && h== glob4 * 3 && i == glob5 - 5 && j == glob6 * 2 && to_spill == glob1 * 4))
        result = 0;


    return result;


}