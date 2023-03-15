int target(void) {
  // we can eliminate both assignments to x
  // (look for: no movl $10, no addition, no inc...no function body basically)
  int x = 10;
  x = x + 1;
  return 5; // return 5, not 0, so it will be set with mov and not xor even if
            // they're being clever
}

int main(void) { return target(); }