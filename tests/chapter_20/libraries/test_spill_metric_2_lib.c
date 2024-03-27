extern int glob1;
extern int glob2;
extern int glob3;
extern int glob4;
extern int glob5;
extern int glob6;

int callee(int ok) {
    if (!ok) {
        // something went wrong already
        return 0;
    }
    glob1 = glob1 / 2;
    glob2 = glob2 - 2;
    glob3 = glob3 + 2;
    glob4 = glob4 / 3;
    glob5 = glob5 + 5;
    glob6 = glob6 / 2;
    return 1;

}