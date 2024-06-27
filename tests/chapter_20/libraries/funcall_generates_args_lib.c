// helper function for funcall_generates_args

#include <stdio.h>
#include <stdlib.h>

// a and b should be 11 and 12
int f(int a, int b) {
    if (a != 11) {
        printf("Expected a to be 11 but found %d\n", a);
        exit(-1);
    }

    if (b != 12) {
        printf("Expected b to be 12 but found %d\n", b);
        exit(-1);
    }

    return 0;
}