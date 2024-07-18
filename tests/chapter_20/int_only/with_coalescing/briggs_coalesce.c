/* Test that we performing coalescing between pseudos that pass the
 * Briggs test. In this case, coalescing lets us get rid of all moves
 * between registers. We inspect the assembly for the target function
 * to validate that it contains no spills and no mov instructions whose source
 * and destination are both general-purpose registers (except mov %rsp, %rbp and
 * mov %rbp, %rsp in the prologue and epilogue)
 * */

#include "../util.h"

int glob7;
int glob8;
int glob9;
int glob10;
int glob11;
int glob12;

int glob = 5;

int target(int one, int two, int three, int four, int five, int six) {
    int seven = (glob - 2) + four;
    int eight = (glob - 1) * two;
    int nine = (glob - 2) * three;
    int ten = (10 - glob) * two;
    int eleven = (glob * two) + one;
    int twelve = (glob + 1) * two;
    glob7 = seven;
    glob8 = eight;
    glob9 = nine;
    glob10 = ten;
    glob11 = eleven;
    glob12 = twelve;
    check_12_ints(one, two, three, four, five, six, 7, 8, 9, 10, 11, 12, 1);
    check_one_int(glob7, 7);
    check_one_int(glob8, 8);
    check_one_int(glob9, 9);
    check_one_int(glob10, 10);
    check_one_int(glob11, 11);
    check_one_int(glob12, 12);
    return 0;
}