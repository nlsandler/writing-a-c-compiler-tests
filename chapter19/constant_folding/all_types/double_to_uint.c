unsigned target(void) { return 2147483750.5; }

int main(void) { return target() == 2147483750u; }