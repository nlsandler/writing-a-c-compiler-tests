struct s;

extern struct s x;
extern struct s y;
int main(void) {
  x = y; // can't assign w/ incomplete struct types
  return 0;
}