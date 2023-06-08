/* Test that we correctly perform conversions "as if by assignment", including:
 * - actual assignment expressions
 * - initializers for automatic variables
 * - return statements
 * Implicit conversions of function arguments are in a separate test case, convert_function_arguments.c
 */

int return_truncated_long(void) {
    long l = 4294967298; // 2^32 + 2
    return l; // this truncates l to an int with value 2
}

long return_extended_int(void) {
    int i = -10;
    return i; // this sign-extends i to a long, preserving its value
}
int main(void) {
    
    /* return_truncated_long() returns 2,
     * the assignment statement converts this to a long
     * but preserves its value.
     */
    long result = return_truncated_long();
    if (result != 2l) {
        return 1;
    }

    /* return_extended_int returns -10 */
    result = return_extended_int();
    if (result != -10) {
        return 2;
    }

    /* This is 2^32 + 2,
     * it will be truncated to 2 by assignment
     */
    int i = 4294967298l;
    if (i != 2) {
        return 3;
    }

    long l = 17179869184l; // 2**34
    /* l will be truncated to 0 on assignment */
    i = l;
    if (i != 0) {
        return 4;
    }

    return 0;
}