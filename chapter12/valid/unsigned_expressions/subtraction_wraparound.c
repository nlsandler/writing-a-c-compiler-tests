int main() {
    unsigned long a = 10ul;
    unsigned long b = 20ul;
    /* a - b = -10
     * Since this number is negative, it wraps around
     * to 2^64 - 10, or 18446744073709551606
     */
    unsigned long result = a - b;
    return (result > a && result > b &&
            result == 18446744073709551606ul);
}