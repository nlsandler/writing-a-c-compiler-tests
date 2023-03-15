int target(int i) {
  unsigned int j = i;
  // don't replace signed w/ unsigned value here
  // NOTE: could handle this if we had separate signed/unsigned operators in
  // TACKY
  return (j > 100);
}

int main(void) { return target(-1); }