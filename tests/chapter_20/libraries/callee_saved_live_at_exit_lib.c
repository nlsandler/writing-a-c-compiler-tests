extern int glob;

int cant_coalesce_fully(int di, int si);

int callee(int a, int b, int c, int d, int e, int f) {
    if (!(a == 1 && b == 2 && c == 3))
        return -1000; // something went wrong

    if (d == -91 && e == 4 && f == 5)
        return 1; // first call

    if (d == 4 && e == -113 && f== 5)
        return 2; // second call

    if (d == 4 && e== 5 && f == -135)
        return 3; // third call


    return -2000; // something went wrong
}

int target(void) {
    int result = cant_coalesce_fully(1, 0);
    if (result != 1)
        return -10;
    if (glob != 6)
        return -11;
    glob = 20; // reset glob to original value
    result = cant_coalesce_fully(0, 1);
    if (result != 2)
        return -12;
    if (glob != 20)
        return -13;
    result = cant_coalesce_fully(0, 0);
    if (result != 3)
        return -14;
    if (glob != 20)
        return -15;
    return 0;
}