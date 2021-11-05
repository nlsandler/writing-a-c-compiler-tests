/* Test that we handle infinity correctly */
int main() {
    double const_inf = 2E308; // this constant will overflow to infinity

    /* make sure that 1/0 is infinity */
    double zero = 0.0;
    double calculated_inf = 1.0 / zero;

    return (calculated_inf > 1E308 && calculated_inf == const_inf);
}