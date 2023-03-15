unsigned long target(void) { return 18446744073709551614ul / 10ul; }

int main(void) { return target() == 1844674407370955161ul; }