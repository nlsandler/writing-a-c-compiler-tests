struct s {
  int x;
};
struct s glob = {0};
struct s f(void) {
  glob.x = glob.x + 1;
  return glob;
}
int main(void) {
  (void)f();
  (void)f();
  return glob.x;
}