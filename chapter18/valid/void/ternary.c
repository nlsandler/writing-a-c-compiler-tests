int i = 0;
int j = 0;
void incr_i() { i = i + 1; }
void incr_j() { j = j + 1; }
int main() {
  1 ? incr_i() : incr_j(); // increment i
  0 ? incr_i() : incr_j(); // increment j
  return (i == 1 && j == 1);
}