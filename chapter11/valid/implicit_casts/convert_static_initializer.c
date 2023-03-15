/* Test that a long static initializer for an int variable
 *  is truncted to an int
 */
int i = 8589934592l; // 2^33, truncated to 0

int main(void) {
    return (i == 0);
}