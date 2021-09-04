/* Test initializing and updating an unsigned global variable */
static unsigned long x = 9223372036854775803ul; // 2^63 - 5

int main() {
    if (x != 9223372036854775803ul)
        return 0;
    x = x + 10;
    if (x != 9223372036854775813ul)
        return 0;
    return 1;
}