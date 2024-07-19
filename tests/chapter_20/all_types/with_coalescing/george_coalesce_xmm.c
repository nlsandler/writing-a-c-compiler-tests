/* Test that we coalesce floating-point pseudos into XMM registers when they
 * pass the George test. In this case, coalescing lets us get rid of all moves
 * between registers. We inspect the assembly for the target function to validate
 * that it contains at most one spill, and no mov instructions whose source and
 * destination are both XMM registers
 * */
#include "../util.h"

double glob = 4.0;


/* 1. Validate eight function parameters.
 *    Purpose: make sure they're coalesced into param-passing registers.
 * 2. Calculate nine pseudoregisters and pass eight of them into
 *    check_eight_doubles.
 *    Purpose: make sure they're coalesced into param-passing registers.
 * 3. Validate ninth pseudoregister.
 *    Purpose: make this pseudoregister conflict with all hard registers,
 *    ensuring that all hard registers have significant degree. This prevents
 *    us from coalescing pseudos into hardregs using the Briggs test, to
 *    force the compiler to use the George test.
 * 4. Call check_one_double and return the result.
 *    Purpose: make sure return value is coalesced into XMM0.
 */
double dbl_target(double a, double b, double c, double d, double e, double f, double g, double h) {
    // Validate parameters a-h (not with check_* functions, to avoid adding
    // new interference)
    if (a != 1.0) {
        return 1.0;
    }
    if (b != 2.0) {
        return 2.0;
    }
    if (c != 3.0) {
        return 3.0;
    }
    if (d != 4.0) {
        return 4.0;
    }
    if (e != 5.0) {
        return 5.0;
    }
    if (f != 6.0) {
        return 6.0;
    }
    if (g != 7.0) {
        return 7.0;
    }
    if (h != 8.0) {
        return 8.0;
    }

    // Now make sure values passed as arguments are coalesced into
    // parameter-passing registers. Calculate using glob so we can't
    // copy prop or constant fold them, and don't need to mov values
    // between registers to calculate them.
    double u = glob - 3.0;      // 1.0
    double v = glob - 2.0;      // 2.0
    double w = glob - 1.0;      // 3.0
    double x = glob * 2.0 - 4.0;  // 4.0
    double y = glob + 1.0;      // 5.0
    double spill = y * 10.0;
    check_14_doubles(u, v, w, x, y, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 1.0);

    // validate spill
    if (spill != 50.0) {
        return 9.0;
    }


    // make sure return value is coalesced into XMM0
    return check_one_double(glob, 4.0);
}

int target(void) {
    // a shim for dbl_target, since wrapper script expects
    // a 'target' function with an integer return value
    return dbl_target(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0);
}
