unsigned long target(void) {
  unsigned long l = -(9223372036854775900ul);
  return l;
}

int main(void) {
  // equivalent test to negate_long
  unsigned long l = target();
  long l2 = (long)l;
  return (l2 - 9223372036854775716l == 0);
}