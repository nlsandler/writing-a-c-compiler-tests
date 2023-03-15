double target(void) { return 10223372036854775816ul; }

int main(void) { return target() == 10223372036854775808.0; }