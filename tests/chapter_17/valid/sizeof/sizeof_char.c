int main(void) {
  signed char x = 0;
  // size of char must be 1
  if (sizeof((char)1) == 1 && sizeof(unsigned char) == 1 && sizeof x == 1)
    return 1;
  return 0;
}