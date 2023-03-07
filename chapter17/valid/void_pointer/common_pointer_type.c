void *calloc(unsigned long nmemb, unsigned long size);
void free(void *ptr);

// the common pointer type of void * and another pointer type is void *
int main() {
  // get a pointer to void
  void *void_ptr = calloc(3, sizeof(unsigned int));
  unsigned int array[3] = {1, 2, 3};

  // like other pointers, void * can be compared to null pointer constant
  if (void_ptr == 0)
    return 0;

  // compare with ==
  if (void_ptr == array)
    return 1;

  // compare with !=
  if (!(void_ptr != array))
    return 1;

  // use in conditional
  // note that result of conditional is void * so it can be implicitly converted
  // to any pointer type

  // also use a void * as the condition here just for fun
  void *null_ptr = 0;
  int *my_array = null_ptr ? void_ptr : array;

  // note: effective type of this object is unsigned int,
  // so we're allowed to access it with an expression of
  // the corresponding signed type, int
  int result = my_array[1];

  free(void_ptr);
  return result;
}