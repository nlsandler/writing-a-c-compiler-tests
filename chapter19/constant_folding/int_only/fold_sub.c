int target() { return 2 - 2147483647; }

int main() { return target() == -2147483645; }