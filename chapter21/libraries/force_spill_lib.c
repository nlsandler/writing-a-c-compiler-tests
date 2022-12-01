extern int glob;
extern int glob2;
int callee(int twelve, int eleven, int ten, int nine, int eight, int seven, int six, int five, int four, int three, int two, int one) {

    glob = 10;
    glob2 = 11;
    if (one == 1 && two == 2 && three == 3 && four == 4 && five == 5 && six == 6 && seven == 7 && eight == 8 && nine == 18 && ten == 10 && eleven == 15 && twelve == 7) {
        // expected results for first call
        return 2;
    }

    if (one == -377 && two == -469 && three == 0 && four == 92 && five == 60 && six == 550 && seven == 81 && eight == 79 && nine == 90 && ten == 2 && eleven == 30 && twelve == 20) {
        // expected results for first call
        return 3;
    }

    return 0;
}