
double callee(double fourteen, double thirteen, double twelve, double eleven, double ten, double nine, double eight, double seven, double six, double five, double four, double three, double two, double one);

double glob = 3.0;
double glob2 = 4.0;

int target(double one, double two, double three, double four, double five, double six)
{
    /* force spill by creating lots of conflicting pseudos
     * validate that we spill the variable should_spill, which is used least
     * and has highest degree
     * Note: this isn't a good test of spill metric calculation;
     * due to optimistic coloring, we could end up spilling just should_spill
     * even if we end up choosing other nodes as spill candidates first
     */
    double should_spill = glob + 3.0;
    // all these registers conflict with should_spill and each other
    double seven = one * one + 6.0;
    double eight = two * 4;
    double nine = three * two * three;
    double ten = four + six;
    double eleven = 16 - five + four;
    double twelve = six + six - five;
    double thirteen = seven + eight;
    double fourteen = nine * ten;

    double result = callee(fourteen, thirteen, twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);

    // make another twelve pseudoes that conflict w/ should_spill and each other
    double fifteen = glob + glob;
    double sixteen = fifteen + 10.0;
    double seventeen = 12.0 - glob;
    double eighteen = sixteen * 3.0;
    double nineteen = eighteen - glob2;
    double twenty = seventeen + nineteen;
    double twenty_one = glob2 * twenty + glob2 * fifteen;
    double twenty_two = result * eighteen;
    double twenty_three = result + eighteen;
    double twenty_four = seventeen - result;
    double twenty_five = twenty - nineteen;
    double twenty_six = twenty_three + twenty_four + twenty_five;
    double twenty_seven = twenty_four * 2.0;
    double twenty_eight = twenty_five * twenty_six;
    double result2 = callee(fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twenty_one, twenty_two, twenty_three, twenty_four, twenty_five, twenty_six, twenty_seven, twenty_eight);
    return should_spill + result2;
}
