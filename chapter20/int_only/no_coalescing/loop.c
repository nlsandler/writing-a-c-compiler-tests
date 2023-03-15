

int flag = 1;
int result = 1;
int a_initialized = 0;

int get(int a, int b, int c, int d, int e, int f) {
    static int call_count = 0;
    call_count = call_count + 1;
    if (call_count == 1) {
        // first call
        if (a == 1 && b == 2 && c == 3 && d == 4 && e == 5 && f == 6)
            return 1;
        else
            return -2;
    } else if (call_count == 2) {
        if (a == 2 && b == 3 && c == 4 && d == 6 && e == 5 && f == 8)
            return 2;
        else
            return -2;
    }
    // if this is call #3, we're done
    flag = 0;
    return 0; // doesn't matter what we return here
}

int target(void) {
    int z;
    int a;
    int tmp1 = 1;
    int tmp2 = 2;
    int tmp3 = 3;
    int tmp4 = 4;
    int tmp5 = 5;
    int tmp6 = 6;
    // make sure our liveness analysis can handle loops correctly:
    // we should recognize that a and z both overlap with tmp1-tmp6 but not each other,
    // so we can avoid any spills by assigning a and z to the same hardreg
    while (flag) {
        if (a_initialized) {
            z = a + 1;
        } else {
            z = 1;
        }
        result = z * result;
        a = get(tmp1, tmp2, tmp3, tmp4, tmp5, tmp6);
        tmp1 = a + 1;
        tmp2 = a + 2;
        tmp3 = a * 4;
        tmp4 = a + 5;
        tmp5 = 6 - a;
        tmp6 = 9 - a;
        a_initialized = 1;
    }
    return result;
}