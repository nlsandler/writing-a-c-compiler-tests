/* Make sure we evaluate the % operator as remainder and not modulo.
 * This is really a constant folding test but requires copy propagation
 * so that we can perform constant folding with negative numbers
 */

int target(void) {
    // the remainder of 6 % -5 is 1
    // 1 = 6 - (-5) * (-1)
    // but 6 modulo -5 is -
    // -4 = 6 - (-5) * (-2)
    return 6 % -5;
}

int main(void) { return target(); }