// make sure we correctly resolve structure tags in derived types

void *malloc(unsigned long size);

struct s {
  int a;
};

int main(void) {
  // pointer to array of three pointers to s
  struct s *(*outer_arr)[3] = malloc(sizeof(void *) * 3);
  struct s outer_struct = {1};
  struct s {
    int x;
  };
  struct s inner_struct = {2};
  struct s *(*inner_arr)[3] = malloc(sizeof(void *) * 3);

  outer_arr[0][0] = &outer_struct;
  outer_arr[0][1] = &outer_struct;

  inner_arr[0][0] = &inner_struct;
  inner_arr[0][2] = &inner_struct;

  return outer_arr[0][0]->a == 1 && inner_arr[0][0]->x == 2;
}