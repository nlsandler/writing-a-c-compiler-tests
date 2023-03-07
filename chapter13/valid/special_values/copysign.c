/* Test that we can check the sign of zero with the copysign function */

// copysign is defined in the C standard library (<math.h>)
double copysign(double x, double y);

int main() {
        // copy the sign from -0.0 to 4.0, producing -4.0
    double negated = copysign(4.0, -0.0);
    double positive = copysign(-5.0, 0.0);
    return (negated == -4.0 && positive == 5.0);
}