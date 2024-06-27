/* Make sure we recognize that EAX is live at exit.
 * Don't inspect assembly; just validate the program's behavior.
 * Note: only works as intended once we've implemented register coalescing.
 * */

#include "../../libraries/util.h"

int glob = 10;
int glob2 = 0;

// The first round of coalescing will coalesce x into EAX.
// Then, if we don't realize that EAX is live at exit, we'll
// coalesce the temporary that holds x + 100 into EAX, clobbering x.

int target(void) {
    int x = glob + 1;  // 11
    glob2 = x + 100;
    return x;
}

int main(void) {
    int retval = target();
    check_one_int(retval, 11);
    check_one_int(glob2, 111);
    return 0;
}