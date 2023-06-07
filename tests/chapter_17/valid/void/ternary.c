int i = 0;
int j = 0;
void incr_i(void) { i = i + 1; }
void incr_j(void) { j = j + 1; }
int main(void) {
  1 ? incr_i() : incr_j(); // increment i
  0 ? incr_i() : incr_j(); // increment j
  return (i == 1 && j == 1);
}