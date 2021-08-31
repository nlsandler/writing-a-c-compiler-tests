/* Test that the value in a 'return' statement is converted to the function's return type. */

long return_extended_int() {
    int i = -10;
    return i; // this sign-extends i to a long, preserving its value
}

int main() {
    long result = return_extended_int();

    return (result == -10);
}