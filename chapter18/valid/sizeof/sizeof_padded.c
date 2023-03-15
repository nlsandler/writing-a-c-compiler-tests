// make sure we calculate size/padding correctly

// need three bytes of padding so it's four-byte aligned,
// total size is eight
struct eightbyte {
  int i;
  char c;
};

struct twobyte {
  char arr[2];
};

struct threebyte {
  char arr[3];
};

struct big {
  struct eightbyte a; // bytes 0-7
  struct twobyte b;   // bytes 8-9
  struct threebyte c; // bytes 10-12
};                    // total size is 16 b/c it's fourbyte aligned

struct medium {
  struct twobyte a;   // bytes 0-1
  struct threebyte b; // bytes 2-4
  struct twobyte c;   // bytes 5-6
};                    // total size is 7 bytes

struct biggest {
  struct medium a; // bytes 0-7
  struct big b;    // bytes 8-24 (four-byte aligned)
};

struct medium_big {
  struct big a;     // bytes 0-16
  struct twobyte b; // bytes 17-18
};                  // 20 bytes b/c it's four-byte aligned

int main(void) {
  if (sizeof(struct twobyte) == 2 && sizeof(struct threebyte) == 3 &&
      sizeof(struct big) == 16 && sizeof(struct medium) == 7 &&
      sizeof(struct biggest) == 24 && sizeof(struct medium_big) == 20) {
    return 1;
  }
  return 0;
}
