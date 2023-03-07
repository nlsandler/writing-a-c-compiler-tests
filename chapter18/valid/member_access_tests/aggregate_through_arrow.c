// test out using/assigning aggregate values through -> pointer

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

void *malloc(unsigned long size);

int main() {
  struct outer *outer_pointer = malloc(sizeof(struct outer));
  outer_pointer->x = 0;
  outer_pointer->y = 0;

  struct inner small = {6, 7, 8};

  outer_pointer->substruct = small;
  if (outer_pointer->substruct.a != 6 || outer_pointer->substruct.b != 7 ||
      outer_pointer->substruct.c != 8 || outer_pointer->x || outer_pointer->y)
    return 1;

  // add another layer of nesting
  struct outermost *outermost_pointer = malloc(sizeof(struct outermost));
  outermost_pointer->i = 0;
  outermost_pointer->nested.substruct = small;
  outermost_pointer->nested.x = -1;
  outermost_pointer->nested.y = -2;

  struct outer copied_from_pointer = outermost_pointer->nested;
  struct inner copied_nested_pointer = outermost_pointer->nested.substruct;

  if (copied_from_pointer.x != -1 || copied_from_pointer.y != -2 ||
      copied_from_pointer.substruct.a != 6 ||
      copied_from_pointer.substruct.b != 7 ||
      copied_from_pointer.substruct.c != 8)
    return 2;

  if (copied_nested_pointer.a != 6 || copied_nested_pointer.b != 7 ||
      copied_nested_pointer.c != 8)
    return 3;
  return 0;
}