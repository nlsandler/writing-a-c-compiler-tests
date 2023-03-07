// make sure we copy correct number of bytes when loading aggregate value from a
// pointer

void *malloc(unsigned long size);

struct chars {
  char char_array[3];
};

int main() {
  // this test relies on the fact that we allocate variables contiguously on the
  // stack make sure copying an aggregate into one object doesn't overwrite the
  // ones next to it
  // it won't test this anymore once we implement register allocation
  char a = 'a';
  char b = 'b';
  char c = 'c';
  struct chars x = {{0, 0, 0}};
  char d = 'd';
  char e = 'e';
  struct chars *ptr = malloc(sizeof(struct chars));
  ptr->char_array[0] = 0;
  ptr->char_array[1] = 1;
  ptr->char_array[2] = 2;
  x = *ptr;
  char f = 'f';
  char g = 'g';
  if (a != 'a' || b != 'b' || c != 'c' || d != 'd' || e != 'e' || f != 'f' ||
      g != 'g')
    return 1;

  if (x.char_array[0] != 0 || x.char_array[1] != 1 || x.char_array[2] != 2)
    return 2;

  return 0;
}