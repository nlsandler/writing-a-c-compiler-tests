unsigned target(void) { return 4294967286u / 10u; }

int main(void) { return target() == 429496728u; }