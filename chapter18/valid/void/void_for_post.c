int i = 0;

void foo() { i = i + 1; }

int main() {
  for (; i < 10; foo())
    ;
  return i;
}