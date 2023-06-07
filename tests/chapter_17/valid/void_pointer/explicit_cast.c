// test explicit casts between void * and other pointer types,
// and between void * and integer types
void *malloc(unsigned long size);
void free(void *ptr);
void *memcpy(void *s1, void *s2, unsigned long n);

int puts(char *c); // for error messages

int main(void) {
  void *ptr = malloc(4 * sizeof(double));
  // cast void * to double *
  double *double_ptr = (double *)ptr;
  double_ptr[2] = 10.0;
  // cast double * back to void * - should round trip
  if ((void *)double_ptr != ptr) {
    puts("Cast from void * to double * and back didn't round trip.");
    return 1;
  }
  double result = double_ptr[2];

  if (result != 10.0) {
    puts("Value in malloc'd array of doubles wasn't preserved.");
    return 2;
  }

  // now test cast from void * to integer
  unsigned long ul = (unsigned long)ptr;
  // address returned by malloc must have suitable alignment
  // for any basic data type, so it's divisible by 8
  if (ul % 8) {
    puts("Value returned by malloc is not eight-byte aligned.");
    return 3;
  }

  free(ptr);
  return 0;
}
