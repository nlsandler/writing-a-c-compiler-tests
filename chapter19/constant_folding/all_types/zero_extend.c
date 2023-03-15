long target(void) { return 4294967295u; }

int main(void) { return target() == 4294967295l; }