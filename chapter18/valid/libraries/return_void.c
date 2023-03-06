void recursive_decrement(unsigned int *ptr) {
  // the least efficient possible way to set an integer to 0
  //  use recursive calls here to make sure we don't mess up
  //  the call stack when calling/returning from void functions
  if (*ptr) {
    *ptr = *ptr - 1;
    recursive_decrement(ptr);
    return;
  }
  return;
}