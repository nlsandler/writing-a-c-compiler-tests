/* Test comparisons on doubles */
int main() {

    // Evaluate true and false case for each comparison operator
    int greater_true = 55e5 > 54e4;
    double four = 4.;
    // make sure we test at least one comparison
    // where the second operand is a variable
    int greater_false = -55e5 > four;

    int less_true = -.00004 < 4.;
    // make sure we test at least one comparison
    // where the first operand is a variabl
    int less_false = four < 4.0;

    int greater_or_equal_true = -10.0 >= -10.0;
    int greater_or_equal_false = 00.00005 >= 5.e3;

    int less_or_equal_true = -25.0 <= -20.0;
    int less_or_equal_false = -25.0 <= -26.0;

    int equal_true = 0.1 == 0.1;
    int equal_false = 0.1 == 0.2;

    int not_equal_true = 10.0 != 1.1e1;
    int not_equal_false = 10.0 != 10.0;

    // Make sure all cases that should be true are true
    int all_trues = greater_true && less_true && greater_or_equal_true
        && less_or_equal_true && equal_true && not_equal_true;

    // make sure all cases that should be false are false
    int any_falses = greater_false || less_false || greater_or_equal_false || less_or_equal_false
        ||  equal_false || not_equal_false;

    return all_trues && !any_falses;
}