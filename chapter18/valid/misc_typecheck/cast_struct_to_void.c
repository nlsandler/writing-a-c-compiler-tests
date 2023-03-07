struct s {
  int x;
};
struct s glob = {0};
struct s f() {
  glob.x = glob.x + 1;
  return glob;
}
int main() {
  (void)f();
  (void)f();
  return glob.x;
}