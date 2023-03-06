struct s {
  int a;
};

struct s x = {1};

int main() {
  x = 0; // can't assign null pointer to struct
  return 0;
}