double d(void) {
    // Implicitly convert this integer to the nearest double,
    // which is 18446744073709551616.0
    return 18446744073709551586ul;
}

int main(void) {
    double retval = d();
    return (retval < 19000000000000000000.0 && retval > 18000000000000000000.0);
}