int main(void) {

  // make sure the result of sizeof is unsigned
  // (if it's not, usual arithmetic conversions will convert
  // operands of <result> > 0 to a signed type and this will be false)
  return sizeof 4 - sizeof 4 - 1 > 0;
}