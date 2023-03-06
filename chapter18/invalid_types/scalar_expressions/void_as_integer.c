// can't use void type where integer is expected

int main() {
  char arr[3];
  return arr[(void)1];
}