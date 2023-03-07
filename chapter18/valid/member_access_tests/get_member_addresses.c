// test applying & to members accessed through . operator,
// and make sure structs are laid out correctly

// need three bytes of padding so it's four-byte aligned,
// total size is eight
struct eightbyte {
  int i;
  char c;
}; // four byte-aligned

struct twobyte {
  char twochars[2];
}; // one byte-aligned

struct threebyte {
  char threechars[3];
}; // one byte-aligned

struct big {
  struct eightbyte eightbyte_1; // bytes 0-7
  struct twobyte twobyte_2;     // bytes 8-9
  struct threebyte threebyte_3; // bytes 10-12
};                              // total size is 16 b/c it's fourbyte aligned

struct medium {
  struct twobyte twobyte_1;     // bytes 0-1
  struct threebyte threebyte_2; // bytes 2-4
  struct twobyte twobyte_3;     // bytes 5-6
};                              // total size is 7 bytes, alignment if 1 byte

struct biggest {
  struct medium medium_1; // bytes 0-7
  struct big big_2;       // bytes 8-24 (four-byte aligned)
};                        // four byte alignment

struct medium_big {
  struct big big_1;         // bytes 0-16
  struct twobyte twobyte_2; // bytes 17-18
};                          // 20 bytes b/c it's four-byte aligned

int main() {
  // declare some static arrays of structs
  static struct medium_big x;

  // x must be four-byte aligned
  // (in our implementation should be eight byte aligned
  // to simplify parameter passing, but ABI doesn't require it)
  if ((unsigned long)&x % 4)
    return 10;

  if ((void *)&x.big_1 != (void *)&x ||
      (void *)&x.big_1.eightbyte_1 != (void *)&x.big_1 ||
      (void *)&x.big_1.eightbyte_1.i != (void *)&x)
    return 1;

  if ((char *)&x.big_1.eightbyte_1.c - (char *)&x != 4)
    return 2;

  if ((char *)&x.big_1.twobyte_2 - (char *)&x != 8)
    return 3;

  if ((void *)&x.big_1.twobyte_2 != &x.big_1.twobyte_2.twochars)
    return 4;

  if ((void *)&x.big_1.twobyte_2 != &x.big_1.twobyte_2.twochars[0])
    return 5;

  if ((char *)&x.big_1.twobyte_2.twochars[1] -
          (char *)&x.big_1.twobyte_2.twochars !=
      1)
    return 6;

  if ((void *)&x.big_1.threebyte_3 != (void *)&x.big_1.threebyte_3.threechars)
    return 7;

  // try one-past-the-end arithmetic
  // no padding b/t big_1 and twobyte_2
  if ((void *)(&x.big_1 + 1) != (void *)&x.twobyte_2)
    return 8;

  if ((void *)(&x.twobyte_2) != (void *)&x.twobyte_2.twochars ||
      (void *)(&x.twobyte_2) != (void *)(&x.twobyte_2.twochars[0]))
    return 9;

  if (&x.twobyte_2.twochars[1] - (char *)&x.twobyte_2.twochars != 1)
    return 11;

  // one-past-the-end arithmetic - should be two bytes of padding b/t end of
  // twochars and end of struct
  if ((char *)(&x + 1) - (char *)(&x.twobyte_2 + 1) != 2)
    return 12;

  // now try a non-static variable
  struct biggest y;
  if ((void *)&y != (void *)&y.medium_1 ||
      (void *)&y != (void *)&y.medium_1.twobyte_1 ||
      (void *)&y != (void *)&y.medium_1.twobyte_1.twochars)
    return 13;

  if ((char *)&y.medium_1.threebyte_2 - (char *)&y.medium_1 != 2)
    return 14;

  if ((char *)(&y.medium_1 + 1) - (char *)&y.medium_1.twobyte_3 != 2)
    return 15;

  return 0;
}