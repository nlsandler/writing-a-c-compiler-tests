/* Test that we recognize call to 'callee' is unreachable;
 * there are two paths to 'exit' but neither will reach it.
 * */

int callee(void) {
    return 100;
}

int target(int a) {
    if (a) {
        return 1;
    } else {
        return 2;
    }

    return callee();  // this should be optimized away
}
int main(void) {
    return (target(1) == 1 && target(0) == 2);
}