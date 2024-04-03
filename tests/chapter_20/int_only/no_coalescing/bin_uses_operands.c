/* Test that we recognize that a binary instruction uses its source and
 * destination; e.g. addl %a, %b makes a and b live. Don't inspect assembly,
 * just validate behavior.
 * NOTE: only works as intended after we've implemented register coalescing.
 */

#include "../../libraries/util.h"

// recognize that add uses its source
int src_test(int i) {
    // this becomes:
    // movl $5, %x
    // addl %i, %x
    // if we don't recognize that addl makes i live, we'll coalesce both
    // i and x into EDI, and check_one_int will fail
    int x = 5 + i;
    check_one_int(x, 6);
    return 0;
}


int glob = 1;
// recognize that sub uses its destination
int dst_test(void) {
    int a = id(100);

    // wrap this in if statement so we can't copy prop temporary values
    // into check_one_int calls below
    if (id(1)) {
        // this addition becomes:
        // movl %a, %tmp
        // addl %glob, %tmp
        // movl %tmp, %glob
        // so we'll coalesce a & tmp unless we recognize that a is still live,
        // which requires us to realize that sub instruction below doesn't kill
        // it
        glob = a + glob;

        // first round of coalescing will coalesce a with
        // temporary result of a - 1, so this will be
        // subl $1, %a.0
        // so we need to recognize that this sub instruction uses a
        a = a - 1;
    }

    check_one_int(a, 99);
    check_one_int(glob, 101);
    return 0;
}

int main(void) {
    src_test(1);
    dst_test();
}