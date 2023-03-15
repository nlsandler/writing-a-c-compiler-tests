long target(void) { return ~100l; }

int main(void) { return target() == -101l; }