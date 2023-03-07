int main() {
    int a = 0;
    double d = 100.0;
    // Use a floating-point number as the controlling expression in a while loop
    // Normally this is a bad idea - rounding error might mean that the value will never
    // be exactly zero, so the loop won't terminate.
    // In this case we won't encounter rounding error, since we can exactly represent
    // every integer between 0 and 100 as a double.
    while (d) {
        a = a + 1;
        d = d - 1.0;
    }
    return a;
}