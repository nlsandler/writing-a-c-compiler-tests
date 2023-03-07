int target() {
  // no je or jne or conditional set instructions, no cmp, at most one jmp
  return 1 && 1;
}

int main() { return target(); }