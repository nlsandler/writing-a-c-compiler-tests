int glob = 20;
int glob2 = 30;
int glob3 = 40;


int target() {
    // create a clique of 7 tmps that interfere
    // we can color all of them w/out spilling anything (includg callee-saved regs)
    int a = glob * glob;
    int b = glob2 + 2;
    int c = a + 5;
    int d = b - glob3;
    int e = glob + 7;
    int f = glob2 * 2;
    int g = c * 3;
    int result;
    if (a == 400 && b == 32 && c == 405 && d == -8 && e == 27 && f == 60 && g == 1215)
        result = 0;
    else {
        result = 1;
    }
    return result;

}