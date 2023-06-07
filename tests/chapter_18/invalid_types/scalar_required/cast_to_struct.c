struct s {
  int a;
};

struct s x;

// can only cast to scalar type or void
// casting struct to itself is illegal
int main(void) { (struct s) x; }