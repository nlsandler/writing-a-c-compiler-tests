/* Make sure our analysis recognizes which registers are used by each function
 * call/return statement - same idea as
 * chapter_20/int_only/no_coalescing/track_arg_registers.c.
 * The test script validates that we don't spill.
 * Liveness analysis should recognize that only XMM0-XMM2 are live right before
 * we call callee(). If we assume XMM3-XMM14 are also live, we'll conclude
 * they're live from the start of the function until the function call
 * (since they're never updated) and won't be able to allocate them, resulting
 * in spills.
 * */

#include "../../libraries/util.h"

// defined in libraries/trakc_dbl_arg_registers_lib.c
int callee(double a, double b, double c);

double glob1;
double glob2;
double glob3;
double glob4;
double glob5;
double glob6;
double glob7;
double glob8;
double glob9;
double glob10;
double glob11;


int target(double one, double two, double three) {
    double four = three + one;
    double five = two + three;
    double six = three * two;
    double seven = 13. - six;
    double eight = four * two;
    double nine = three * three;
    double ten = five * two;
    double eleven = seven * two - three;
    double twelve = eight * four - 20.;
    double thirteen = (nine + ten) - six;
    double fourteen = eleven + 3;

    // copy variables into global variables to make them interfere
    glob1 = one;
    glob2 = two;
    glob3 = three;
    glob4 = four;
    glob5 = five;
    glob6 = six;
    glob7 = seven;
    glob8 = eight;
    glob9 = nine;
    glob10 = ten;
    glob11 = eleven;

    // don't need to copy in twelve through fourteen b/c we use them below

    // use ten through twelve
    callee(twelve, thirteen, fourteen);

    // validate globals
    check_14_doubles(glob1, glob2, glob3, glob4, glob5, glob6, glob7, glob8, glob9, glob10, glob11, 12., 13., 14., 1);

    return 0;
}
