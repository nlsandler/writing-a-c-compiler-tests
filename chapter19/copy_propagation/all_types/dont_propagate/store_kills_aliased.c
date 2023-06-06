int aliased_src(int x) {
    int y = x; // src is aliased
    static int unused;
    int *ptr = &unused;
    if (x) {
        ptr = &x;
    }
    *ptr = 100;
    if (y != 12) {
        return 1;
    }
    return 0;
}

int aliased_dst(int flag)
{
    // store instructions kills any copies with aliased destination
    int i = 10;
    int j = 20;

    // alias i and j
    int *ptr1 = &i;
    int *ptr2 = &j;
    // kill i = 10 and j = 20
    int *ptr = flag ? ptr1 : ptr2;
    *ptr = 100;


    // validate results
    if (flag) {
        // i should be 100, j should be unchanged
        if (i != 100) {
            return 2;
        }
        if (j != 20) {
            return 3;
        }
    } else {
        // j should be 100, i should be unchanged
        if (j != 100) {
            return 4;
        }
        if (i != 10) {
            return 5;
        }

    }
    return 0;
}

int main(void) {
    int status = aliased_src(12);
    if (status) {
        return status;
    }
    status = aliased_dst(0);
    if (status) {
        return status;
    }
    return aliased_dst(1);
}