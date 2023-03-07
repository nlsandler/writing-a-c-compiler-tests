struct s; // declare incomplete structure type

struct a {
  // can't use incomplete struct type as member
  struct s g;
};