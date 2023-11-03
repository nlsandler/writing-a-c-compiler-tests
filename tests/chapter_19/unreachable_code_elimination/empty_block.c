/* Test that having empty blocks after optimization doesn't break anything;
 * after removing useless jumps and labels, 'target' will contain several
 * empty basic blocks.
 * */

int target(int x, int y) {
    if (x) {
        if (y) {
        }
    }
    return 1;
}

int main(void) {
    return target(1, 1) == 1 && target(0, 0) == 1;
}