/* Test that we correctly handle negative infinity */
int main() {
    double negated_inf = -2E308;

    /* make sure that -1/0 is negative infinity */
    double zero = 0.0;
    double calculated_neg_inf = -1.0 / zero;

    return (calculated_neg_inf < -1E308 && calculated_neg_inf == negated_inf);
}