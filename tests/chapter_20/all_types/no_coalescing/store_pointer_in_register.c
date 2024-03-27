/* writing thorugh a pointer doesn't update register holding the pointer, e.g.
 * movq %ptr, %r
 * mov %src, (%r)
 * ... use ptr
 * does not create conflict b/t %ptr and %r
 *
 * need to create an interference graph that's only colorable if we assign ptr
 * to r
 * ...but we don't know what r is
 */

int glob;
int glob2;
int glob3;
int glob4;
int glob5;
int glob6;
int glob7;

int flag = 1;

int *store_a;

int target(void) {
  // create a clique of 7 tmps that interfere
  // each tmp is a pointer that we write through, whcih remains live afterwards
  // this is colorable w/out spills as long as none of these conflict with the
  // register we load pointers into
  int *a;
  int *b;
  int *c;
  int *d;
  int *e;
  int *f;
  int *g;
  // use flag to avoid copy prop
  if (flag) {
    a = &glob;
    *a = 1;
    b = &glob2;
    *b = 2;
    c = &glob3;
    *c = 3;
    d = &glob4;
    *d = 4;
    e = &glob5;
    *e = 5;
    f = &glob6;
    *f = 6;
    g = &glob7;
    // every tmp will conflict with the register we load pointers into, except g
    // (b/c g isn't live while we load earlier pointers into that register)
    *g = 7;
    // store a to a global variable so that all regs conflict but we'll have lower
    // register pressure later when we do comparisons
    store_a = a;

  } else {
    a = 0;
    b = 0;
    c = 0;
    d = 0;
    e = 0;
    f = 0;
    g = 0;
  }

  if (b != &glob2 || c != &glob3 || d != &glob4 || e != &glob5 ||
      f != &glob6 || g != &glob7) {
    return 1;
  }
  if (glob != 1 || glob2 != 2 || glob3 != 3 || glob4 != 4 || glob5 != 5 ||
      glob6 != 6 || glob7 != 7) {
    return 2;
  }
  if (store_a != &glob) {
    return 3;
  }
  return 0;
}
