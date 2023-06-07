unsigned long target(void) { return -1000; }

int main(void) { return target() == 18446744073709550616ul; }