unsigned char target() {
  unsigned char c = (unsigned char)9223372036854775716l;
  return c;
}
int main() { return (int)target() == 164; }