struct s;

extern struct s x; // declare but don't define

int get_member(struct s *param);

int main(void) { return get_member(&x); }

// define the struct
struct s {
  int a;
};

// define x
struct s x = {100};
int get_member(struct s *param) { return param->a; }