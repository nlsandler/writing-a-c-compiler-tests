
int callee(int twelve, int eleven, int ten, int nine, int eight, int seven, int six, int five, int four, int three, int two, int one);

int glob = 3;
int glob2 = 4;

int target(int one, int two, int three, int four, int five, int six)
{
    /* force spill by creating lots of conflicting pseudos
     * validate that we spill the variable should_spill, which is used least
     * and has highest degree
     * Note: this isn't a good test of spill metric calculation;
     * due to optimistic coloring, we coudl end up spilling just should_spill
     * even if we end up choosing other nodes as spill candidates first
     */
    int should_spill = glob + 3;
    // all these registers conflict with should_spill and each other
    int seven = one * one + 6;
    int eight = two * 4;
    int nine = three * two * three;
    int ten = four + six;
    int eleven = 16 - five + four;
    int twelve = six + six - five;

    int result = callee(twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);

    // make another twelve pseudoes that conflict w/ should_spill and each other
    int thirteen = glob + glob;
    int fourteen = thirteen + 10;
    int fifteen = 12 - glob;
    int sixteen = fourteen * 3;
    int seventeen = sixteen - glob2;
    int eighteen = fifteen + seventeen;
    int nineteen = glob2 * fourteen + glob2 * thirteen;
    int twenty = result * fourteen;
    int twenty_one = result + sixteen;
    int twenty_two = fifteen - result;
    int twenty_three = eighteen - nineteen;
    int twenty_four = twenty_one + twenty_two + twenty_three;
    int result2 = callee(thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twenty_one, twenty_two, twenty_three, twenty_four);
    return should_spill + result2;
}
