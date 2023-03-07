// we can coalesce all the temporary variables we generate during TACKY generation

int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 0;

int briggs() {
    int a = (glob1 * 3) + (glob2 * 4) + (glob3 * 5) + (glob4 * 6);
    int b = a * 10;
    glob5 = b;
    return 0;
}

int target() {
    briggs();
    return (glob5 == 500);
}