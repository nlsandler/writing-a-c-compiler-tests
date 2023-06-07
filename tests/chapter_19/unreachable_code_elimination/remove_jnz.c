/* Test that we eliminate useless JumpIfNotZero */
int target(int a) { return a || 5; }

int main(void) { return target(10); }