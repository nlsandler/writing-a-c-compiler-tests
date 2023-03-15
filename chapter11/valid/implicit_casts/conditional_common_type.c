int main(void) {
    long l = 8589934592l; // 2^33
    int i = 10;

    /* When a conditional expression includes both int and long branches,
     * make sure the int type is promoted to a long, rather than the long being
     * converted to an int 
     */
    long result = 1 ? l : i;

    return (result == 8589934592l);
}