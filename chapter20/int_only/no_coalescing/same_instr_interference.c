/* test that addl x, y (or similar) causes interference b/t x and y if x is live afterward
 * just test for correctness  */

int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;

// use this to force pseudoregs to be callee-saved
int reset_globals(void) {
  glob0 = 0;
  glob1 = 0;
  glob2 = 0;
  glob3 = 0;
  glob4 = 0;
  glob5 = 0;
  return 0;
}

int use_value(int v) {
  glob0 = glob0 + v;
  return 0;
}

int target(void) {
  /* define some values - must be in calle-saved regs */
  int a = glob0;
  int b = glob1;
  int c = glob2;
  int d = glob3;
  reset_globals();
  int e = a * a; // now e interferes w/ a, b, c, and d
  use_value(a);
  int f = b * b; // now f interferes w/ b, d, c and e but not a
  use_value(b);
  int g = c * c; // g interferes with c, d, e, f but not a or b
  use_value(c);
  int h = d * d; // h interferes with d, e, f, g but not a, b, c
  use_value(d);
  int result = 0;
  if (e != 0) {
    result = 1;
  } else if (f != 1) {
    result = 2;
  } else if (g != 4) {
    result = 3;
  } else if (h != 9) {
    result = 4;
  } else {
    result = glob0;
  }
  return result;
}

int main(void) { return target(); }