/* Test that we eliminate useless JumpIfNotZero */

#if defined SUPPRESS_WARNINGS && defined __clang__
#pragma clang diagnostic ignored "-Wconstant-logical-operand"
#endif
int target(int a) { return a || 5; }

int main(void) { return target(10); }