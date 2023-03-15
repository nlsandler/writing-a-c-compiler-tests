/* Make sure we use optimistic coloring:
 * Include:
 *     - Pseudos with low cost and short live ranges which will spill first but
 * don't decrease register pressure
 *     - Pseudos with high cost and long live ranges which spill later
 * Make sure we color the low-cost ones!
 * What if we had: clique ABCDE, clique EFGHI, and clique JKLMN that conflicts
 * with all of them make sure ABCDE have lowest spill cost, so we choose them as
 * spill candidates first then we choose JKLMN as next batch of spill candidates
 * then we prune the rest of the graph
 * then we actually spill JKLMN, which lets us color ABCDE
 */

int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 0;
int glob6 = 0;
int glob7 = 0;
int glob8 = 0;
int glob9 = 0;

int flag = 0;
int result = 0;
int increase_globals(void) {
  glob0 = glob0 + 1;
  glob1 = glob1 + 1;
  glob2 = glob2 + 1;
  glob3 = glob3 + 1;
  glob4 = glob4 + 1;
  return 0;
}

int reset_globals(void) {
  glob0 = 0;
  glob1 = 1;
  glob2 = 2;
  glob3 = 3;
  glob4 = 4;
  glob5 = 0;
  glob6 = 0;
  glob7 = 0;
  glob8 = 0;
  glob9 = 0;
  return 0;
}

int get(void) {
  static int i = 100;
  i = i + 3;
  return i;
}

int use(int one, int two, int three, int four, int five) {
  glob5 = glob5 + one;
  glob6 = glob6 + two;
  glob7 = glob7 + three;
  glob8 = glob8 + four;
  glob9 = glob9 + five;
  return 0;
}

int validate_globs(int one, int two, int three, int four, int five) {
    if (glob5 != one)
        return 10;
    if (glob6 != two)
        return 12; 
    if (glob7 != three)
        return 13; 
    if (glob8 != four)
        return 14; 
    if (glob9 != five)
        return 15;
    return 0;
}

int five_spills(void) {
  // k - o conflict with everything, have higher spill metric than a-e but lower
  // than f-j
  int k = get();
  int l = get();
  int m = get();
  int n = get();
  int o = get();
  if (!flag) {
    // make a-e a clique with low spill cost
    int a = glob0;
    int b = glob1;
    int c = glob2;
    int d = glob3;
    int e = glob4;
    increase_globals();
    use(k, l, m, n, o);
    result = a == glob0 - 1 && b == glob1 - 1 && c == glob2 - 1 &&
             d == glob3 - 1 && e == glob4 - 1 && k - glob0 == 102 &&
             l / glob1 == 53 && m % glob2 == 1 && n + glob3 == 116 &&
             o % glob4 == 0;
    ;
  } else {
    // make F-I a clique with higher spill cost
    int f = glob0;
    int g = glob1;
    int h = glob2;
    int i = glob3;
    int j = glob4;
    increase_globals();
    use(f, g, h, i, j);
    use(g, h, i, j, f);
    use(h, i, j, f, g);
    use(i, j, f, g, h);
    use(j, f, g, h, i);
    f = f + 1;
    g = g + 1;
    h = h + 1;
    j = j + 1;
    i = i + 1;
    result = f == glob0 && g == glob1 && h == glob2 && i == glob3 &&
             j == glob4 && k - glob0 == 117 &&
             l + glob1 == 123 && m % glob2 == 1 && n + glob3 == 131 &&
             o % glob4 == 0;
  }

  return result;
}

int target(void) {
  reset_globals();
  flag = 0;
  int retval = five_spills();
  if (!retval)
    return 1;
  int globs_expected = validate_globs(103, 106, 109, 112, 115);
  if (globs_expected)
    return globs_expected + 100;
  reset_globals();
  flag = 1;
  retval = five_spills();
  if (!retval)
    return 2;
  return validate_globs(10, 10, 10, 10, 10);
}