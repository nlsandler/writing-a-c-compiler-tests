/* Test that we performing coalescing between floating-point pseudos that pass
 * the Briggs test.
 */

#include "../util.h"

double glob = 5.;

double glob9;
double glob10;
double glob11;
double glob12;
double glob13;
double glob14;


int target(double one, double two, double three, double four, double five, double six, double seven, double eight) {
    double nine = (glob - two) * 3.;
    double ten = (glob * four) / 2.;
    double eleven = (18. - eight) + one;
    double twelve = 11. * one + one;
    double thirteen = (2. * two) + 9.;
    double fourteen = (3. + four) * 2;
    glob9 = nine;
    glob10 = ten;
    glob11 = eleven;
    glob12 = twelve;
    glob13 = thirteen;
    glob14 = fourteen;

    check_14_doubles(one, two, three, four, five, six, seven, eight, 9., 10., 11., 12., 13., 14., 1.);
    check_one_double(glob9, 9.);
    check_one_double(glob10, 10.);
    check_one_double(glob11, 11.);
    check_one_double(glob12, 12.);
    check_one_double(glob13, 13.);
    check_one_double(glob14, 14.);
    return 0;
}