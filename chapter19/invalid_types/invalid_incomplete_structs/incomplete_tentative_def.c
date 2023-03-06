struct s;

// it's illegal to define a variable w/ an incomplete structure type
// (some compilers allow tentative defs if var has external linkage
// and the  type is completed
// later in the same translation unit, but we don't.)
static struct s x;

int main() { return 0; }