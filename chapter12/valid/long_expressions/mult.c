int main() {
    long int a = 4294967290l;
    /* Multiplying two longs should produce the correct result,
     * even when that result is too large for an int to represent 
     */    
    if (a * 4l == 17179869160l) {
        return 1;
    }
    return 0;
}