/* Test that we performing coalescing between pseudos that pass the
 * Briggs test. In this case, coalescing lets us get rid of all moves
 * between registers. We inspect the assembly for the target function
 * to validate that it contains no spills and no mov instructions whose source
 * and destination are both general-purpose registers (except mov %rsp, %rbp and
 * mov %rbp, %rsp in the prologue and epilogue)
 * */

#include "../../libraries/util.h"

int glob0;
int glob1;
int glob2;
int glob3;
int glob4;
int glob5;
int one = 1; // define a value we can't constant fold or propagate

// call this to prevent copy prop into function calls
int update_glob5(void) {
    glob5 = 100;
    return 0;
}

int target(void) {
    // define five pseudos that will all interfere
    int a;
    int b;
    int c;
    int d;
    int e;

    /* On each loop iteration, we initialize one variable
    * with a complex expression that requires an intermediate result;
    * the pseudoregister holding this result should be coalesced into that
    * variable. We then initialize the other four variables with constants.
    * At the end of each loop iteration we validate all five variables.
    * The intermediate results don't interfere with any other pseudos.
    *
    * The reason this test coalesces temporary values into five different
    * variables, which must all be placed in different registers, is to
    * validate that we actually performed coalescing, and didn't just happen
    * to assign a variable and the corresponding intermediate result to the
    * same hard register. (If this test program had less register pressure,
    * just assigning every pseudo the lowest available color might get rid of
    * every mov instruction even if we didn't actually perform coalescing.)
    * */

    static int x; // make this static so it doesn't affect register allocation

    for (x = 0; x < 5; x = x + 1) {
        if (!x) {
            // movl  $10, %tmp1
            // imull %one, %tmp1
            // movl  %tmp1, %tmp2
            // addl  $1, %tmp2
            // movl  %tmp2, %a

            // Make sure we coalesce tmps into a
            a = 10 * one + 1;
            b = 2;
            c = 3;
            d = 4;
            e = 5;
        }
        if (x == 1) {
            // movl  $20, %tmp1
            // imull %one, %tmp1
            // movl  %tmp1, %tmp2
            // addl  $1, %tmp2
            // movl  %tmp2, %b

            // Make sure we coalesce tmps into b
            b = 20 * one + 1;
            a = 1;
            c = 3;
            d = 4;
            e = 5;
        }
        if (x == 2) {
            // movl  $30, %tmp1
            // imull %one, %tmp1
            // movl  %tmp1, %tmp2
            // addl  $1, %tmp2
            // movl  %tmp2, %c

            // Make sure we coalesce tmps into c
            c = 30 * one + 1;
            a = 1;
            b = 2;
            d = 4;
            e = 5;
        }
        if (x == 3) {
            // movl  $40, %tmp1
            // imull %one, %tmp1
            // movl  %tmp1, %tmp2
            // addl  $1, %tmp2
            // movl  %tmp2, %d

            // Make sure we coalesce tmps into d
            d = 40 * one + 1;
            a = 1;
            b = 2;
            c = 3;
            e = 5;
        }
        if (x == 4) {
            // movl  $50, %tmp1
            // imull %one, %tmp1
            // movl  %tmp1, %tmp2
            // addl  $1, %tmp2
            // movl  %tmp2, %e

            // Make sure we coalesce tmps into e
            e = 50 * one + 1;
            a = 1;
            b = 2;
            c = 3;
            d = 4;
        }
        /* Save a-e to global variables; don't pass them directly to
         * check_one_int beause we don't want any moves between registers.
         * This also makes a-e interfere with each other.
         * */
        glob0 = a;
        glob1 = b;
        glob2 = c;
        glob3 = d;
        glob4 = e;
        // call a function to prevent copy propagation of a-e into calls below
        update_glob5();
        // validate values of a-e
        check_one_int(glob0, x == 0 ? 11 : 1);
        check_one_int(glob1, x == 1 ? 21 : 2);
        check_one_int(glob2, x == 2 ? 31 : 3);
        check_one_int(glob3, x == 3 ? 41 : 4);
        check_one_int(glob4, x == 4 ? 51 : 5);
        check_one_int(glob5, 100); // this just validates that we actually called update_glob5
    }

    return 0;
}
