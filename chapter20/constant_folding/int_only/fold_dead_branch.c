int target() {
  // look for:
  // - jmp lbl instead of je lbl
  // - no cmpl instructions
  if (0)
    return 1;
  return 0;
}

int main() { return target(); }