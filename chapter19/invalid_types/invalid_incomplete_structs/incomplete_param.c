struct s;

// it's illegal to define a function with an incomplete parameter
int foo(struct s x) { return 0; }
