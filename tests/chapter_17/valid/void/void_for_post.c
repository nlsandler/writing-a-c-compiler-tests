int i = 0;

void foo(void) { i = i + 1; }

int main(void) {
  for (; i < 10; foo())
    ;
  return i;
}