/* Test that the value in a 'return' statement is converted to the function's return type. */

int return_truncated_long(void) {
    long l = 4294967298; // 2^32 + 2
    return l; // this truncates l to an int with value 2
}

int main(void) {
    /* return_truncated_long() returns 2,
     * the assignment statement converts this to a long
     * but preserves its value.
     */
    long result = return_truncated_long();

    return (result == 2l);
}