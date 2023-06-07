// test that we can constant fold casts b/t int and uint, allowing for further
// copy propagation

unsigned int target(void) {
  int i = -1;
  unsigned int u = (unsigned)i;
  return u - 10;
}

int main(void) { return target() == 4294967285u; }