struct s {
  double d;
  void *arr[3];
};

// can't initialize void * w/ double
struct s x = {0.0, {1.0}};