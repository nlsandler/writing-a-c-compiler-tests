int main(void) {
    long a = 4294967290l;
    long b = 5l;
    /* Adding two longs should produce the correct result,
     * even when that result is too large for an int to represent 
     */
    if (a + b == 4294967295l) {
        return 1;
    }
    return 0;
}