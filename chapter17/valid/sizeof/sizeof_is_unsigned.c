int puts(char *c); // for error messages

int main(void) {

  // make sure the result of sizeof is unsigned
  // (if it's not, usual arithmetic conversions will convert
  // operands of <result> > 0 to a signed type and this will be false)
  if (sizeof 4 - sizeof 4 - 1 < 0) {
    puts("Result of sizeof should be unsigned, but it's signed.");
    return 1;
  }

  if (sizeof(sizeof 0) != 8) {
    puts("Result of sizeof shoudl be an unsigned long but it's not an "
         "eight-byte object.");
    return 2;
  }
  return 0;
}