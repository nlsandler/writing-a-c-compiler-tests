double copysign(double x, double y);

double target(int flag) {
  double result = 0.0;
  if (flag) {
    result = -0.0;
  }
  return result; // can't propagate because 0.0 and -0.0 are different!
}

int main() {
  double pos_inf = 1 / target(0);
  double neg_inf = 1 / target(1);
  return pos_inf > neg_inf;
}