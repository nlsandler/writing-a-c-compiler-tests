// validation helper function used by a few tests

// okay to use standard library b/c we compile this file with
// the system compiler, not the reader's compiler
#include <stdio.h>
#include <stdlib.h>

int check_one_int(int actual, int expected) {
    if (actual != expected) {
        printf("Expected %d but found %d\n", expected, actual);
        exit(-1);
    }
    return 0;
}

// validates a == start, b == start + 1, ...e == start + 5
// and exits early if they don't have those values
int check_5_ints(int a, int b, int c, int d, int e, int start) {
    // validate that a == start + 11, b == start + 10, ...l == start
    int args[5] = {a, b, c, d, e};
    for (int i = 0; i < 5; i++) {
        int expected = start + i;
        if (args[i] != expected) {
            printf(
                "Expected argument %d to have value %d, actual value was %d\n",
                i, start + i, args[i]);
            exit(-1);
        }
    }

    return 0;  // success
}

// validates a == start, b == start + 1, ... l == start + 11
// and exits early if they don't have those values
// TODO refactor pre-chapter-20 tests that define check_12_ints to use this
// library instead?
int check_12_ints(int a, int b, int c, int d, int e, int f, int g, int h, int i,
                  int j, int k, int l, int start) {
    // validate that a == start + 11, b == start + 10, ...l == start
    int args[12] = {a, b, c, d, e, f, g, h, i, j, k, l};
    for (int i = 0; i < 12; i++) {
        int expected = start + i;
        if (args[i] != expected) {
            printf(
                "Expected argument %d to have value %d, actual value was %d\n",
                i, start + i, args[i]);
            exit(-1);
        }
    }

    return 0;  // success
}

int id(int x) {
    return x;
}