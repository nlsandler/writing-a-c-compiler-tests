int main() {
    long a = -4294967290l;
    long b = 90l;
    /* Subtracting two longs should produce the correct result */
    if (a - b == -4294967380l) {
        return 1;
    }
    return 0;
}