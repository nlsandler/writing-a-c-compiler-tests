int main(void) {
    unsigned int x = 10;
    /* Test out rewrite rule for addition;
     * even when adding numbers we interpret as unsigned,
     * the 'add' instruction can only handle immediate values
     * that fit into a signed int
     */
    unsigned long y = x + 4294967295; // 2^32 - 1 is UINT_MAX
    return (y == 4294967305);
}