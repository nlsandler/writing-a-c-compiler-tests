int non_zero(double d) {
    return !d;
}

int main(void) {

    /* Make sure subnormal numbers are not rounded to zero */
    double subnormal = 2.5e-320;

    // subnormal is non-zero, so !subnormal should be zero
    return non_zero(subnormal);
}