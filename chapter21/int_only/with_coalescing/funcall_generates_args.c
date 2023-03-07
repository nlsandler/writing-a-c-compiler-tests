int f(int a, int b);

int glob = 10;

int target() {
    static int x;
    static int y;
    int a = glob + 1;
    int b = glob + 2;
    // we'll coalesce a and b with edi/esi b/c they're passed as params
    // and, if we don't recognize that EDI/ESI are live, we'll _ALSO_
    // coalesce the temporaries that hold a * glob and b * glob with EDI/ESI too
    x = a * glob;
    y = b * glob;
    int result = f(a, b);
    // return result ==1 && x == 110 && y == 120;
    if (result != 1)
        return 1;
    if (x != 110)
        return 2;
    if (y != 120)
        return 3;
    return 0;
}