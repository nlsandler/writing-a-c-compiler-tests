struct s {
  int y;
};

struct s x;
// dot operator must be immediately followed by field name
//  (can't parenthesize it)
int main() { return x.(y); }
