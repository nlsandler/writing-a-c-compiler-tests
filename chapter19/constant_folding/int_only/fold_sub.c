int target(void) { return 2 - 2147483647; }

int main(void) { return target() == -2147483645; }