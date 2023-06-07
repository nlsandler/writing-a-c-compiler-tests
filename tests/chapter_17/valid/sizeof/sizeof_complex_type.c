int main(void) {
  // get size of type specified by complex abstract declarator
  // this is an array of 3 arrays of 4 pointers, for total size
  // 3 * 4 * 8 = 96
  // (each pointer points to an array of two doubles
  // but that doesn't impact the overall size)
  return sizeof(double(*([3][4]))[2]);
}