char target() {
  char c = (char)9223372036854775716l;
  return c;
}
// TODO I don't think this really tests what we want
int main() { return (int)target() == -92; }