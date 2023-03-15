// test explicit casts between void * and other pointer types,
// and between void * and integer types
void *malloc(unsigned long size);
void free(void *ptr);
void *memcpy(void *s1, void *s2, unsigned long n);

int main(void) {
  void *ptr = malloc(4 * sizeof(double));
  // cast void * to double *
  double *double_ptr = (double *)ptr;
  double_ptr[2] = 10.0;
  // cast double * back to void * - should round trip
  if ((void *)double_ptr != ptr)
    return 0;
  double result = double_ptr[2];

  if (result != 10.0)
    return 0;

  // now test cast from void * to integer
  unsigned long ul = (unsigned long)ptr;
  // address returned by malloc must have suitable alignment
  // for any basic data type, so it's divisible by 8
  if (ul % 8)
    return 0;

  free(ptr);
  return 1;
}
