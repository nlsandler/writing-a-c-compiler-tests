extern int glob;
extern int glob2;
int callee(unsigned int twelve, double *eleven, int ten, signed char nine, int *eight, unsigned long seven, long six, unsigned int five, long four, unsigned int three, int two, unsigned char one) {

    glob = 10;
    glob2 = 11;
    if (one == 1 && two == 2 && three == 3 && four == 4 && five == 4294967295u && six == 8 && seven == 7 && *eight == 10 && nine == 8 && ten == 12 && *eleven == 5. && twelve == 1) {
        // expected results for first call
        return 2;
    }

    if (one == 62 && two == -158 && three == 0 && four == 62 && five == 40 && six == 220 && seven == 62 && *eight == 11 && nine == 60 && ten == 2 && *eleven == 5. && twelve == 20) {
        // expected results for first call
        return 3;
    }

    return 0;
}