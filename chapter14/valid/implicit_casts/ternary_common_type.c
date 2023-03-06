/* Test that we perform the usual arithmetic operations correctly in ternary expressions */
int main() {
    // If the first operand of a ternary operator is a double,
    // you don't need to convert the second and third operands to double.
    // In this case we'll converting the second and third operands to the common type
    // of int and unsigned long, which is unsigned long. THEN this is converted
    // to a double when assigned to x.
    double x = 2.0 ? -30 : 10ul;

    // If the second operand of a ternary operator is a double,
    // you must convert the third operand to double, and vice versa.
    double y = 0 ? 5.0 : 9223372036854777850ul;

    // Converting -30 to unsigned long gives us 2^64 - 30
    // Converting 9223372036854777850 to a double gives us
    // 9223372036854777856.0
    return x == 18446744073709551586.0 &&
        y == 9223372036854777856.0;
}