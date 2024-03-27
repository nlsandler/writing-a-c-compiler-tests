extern double glob;
extern double glob2;
double callee(double fourteen, double thirteen, double twelve, double eleven, double ten, double nine, double eight, double seven, double six, double five, double four, double three, double two, double one) {

    glob = 10;
    glob2 = 11;
    if (one == 1 && two == 2 && three == 3 && four == 4 && five == 5 && six == 6 && seven == 7 && eight == 8 && nine == 18 && ten == 10 && eleven == 15 && twelve == 7 && thirteen == 15. && fourteen == 180.) {
        // expected results for first call
        return 2;
    }

    if (one == 188 && two == 0 && three == 94 && four == 2 && five == 0 && six == 92 && seven == 180 && eight == 1111 && nine == 81 && ten == 79 && eleven == 90 && twelve == 2 && thirteen == 30 && fourteen == 20) {
        // expected results for second call
        return 3;
    }

    return 0;
}