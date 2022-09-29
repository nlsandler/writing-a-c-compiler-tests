struct s;

extern struct s x;

int main() {
  // can't use variable w/ incomplete struct type as expression statement
  for (x;;)
    ;
  return 0;
}