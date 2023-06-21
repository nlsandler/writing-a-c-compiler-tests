#ifdef SUPPRESS_WARNINGS
#ifdef __clang__
#pragma clang diagnostic ignored "-Wincompatible-library-redeclaration"
#else
#pragma GCC diagnostic ignored "-Wbuiltin-declaration-mismatch"
#endif
#endif

void *malloc(unsigned long size);
void free(void *ptr);
int memcmp(void *s1, void *s2, unsigned long n);
// make sure we can implicitly convert to and from void * by assignment
void *return_ptr(char *i) {
  // get pointer to i[3], implicitly cast from char * to void *
  return i + 3;
}

int main(void) {
  void *four_bytes = malloc(4);
  // implicitly convert void * to int *
  int *int_ptr = four_bytes;
  *int_ptr = -1; // set all bits to 1

  // implicitly convert four_bytes from void * to char *
  // by passing it as a function argument
  void *last_byte = return_ptr(four_bytes);

  char *last_char = last_byte;

  if (*last_char != -1)
    return 0;

  free(four_bytes);

  long arr1[3] = {1, 2, 3};
  long arr2[3] = {1, 2, 3};
  long arr3[3] = {1, 2, 4};
  return memcmp(arr1, arr2, sizeof arr1) == 0 &&
         memcmp(arr1, arr3, sizeof arr2) == -1;
}
