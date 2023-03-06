struct inner {
  signed char a;
  signed char b;
  signed char c;
};

struct outer {
  struct inner substruct;
  signed char x;
  signed char y;
};

struct outermost {
  struct outer nested;
  int i;
};

int main() {
  static struct outer big_struct = {{0, 0, 0}, 0, 0};
  struct inner small_struct = {-1, -2, -3};
  big_struct.substruct = small_struct;
  // make sure we updated substruct w/out overwriting other members
  if (big_struct.substruct.a != -1 && big_struct.substruct.b != -2 &&
      big_struct.substruct.c != -3)
    return 1;
  if (big_struct.x || big_struct.y)
    return 2;

  // now try w/ multiple levels of nesting (and w/ auto storage duratioN)
  struct outermost biggest_struct = {big_struct, -1};
  small_struct.a = 50;
  small_struct.b = 51;
  small_struct.c = 52;
  biggest_struct.nested.substruct = small_struct;

  if (biggest_struct.nested.x || biggest_struct.nested.y)
    return 3;
  if (biggest_struct.i != -1)
    return 4;

  struct inner copied_from_biggest = biggest_struct.nested.substruct;
  if (copied_from_biggest.a != 50 || copied_from_biggest.b != 51 ||
      copied_from_biggest.c != 52)
    return 5;

  return 0;
}