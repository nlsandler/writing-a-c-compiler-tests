// make sure we rewrite push instructions involving xmm registers

int callee(double a, double b, double c, double d, double e, double f, double g,
           double h, double i, double j, double k) {
  if (a == 0. && b == 1. && c == 2. && d == 3. && e == 4. && f == 5. &&
      g == 6. && h == 7. && i == 8. && j == 9. && k == 10.)
    return 1;
  return 0;
}

int target(int a, int b, int c, int d, int e) {
  return callee(0., 1., 2., 3., 4., 5., e + 1., d + 3., c + 5., b + 7., a + 9.);
}
