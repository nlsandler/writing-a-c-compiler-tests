// make sure we allocate all integer types together (this is the same as int_only force_spill.c but with a mix of types)


long callee(unsigned int twelve, double *eleven, int ten, signed char nine, int *eight, unsigned long seven, long six, unsigned int five, long four, unsigned int three, int two, unsigned char one);

int glob = 3;
int glob2 = 4;
double glob3 = 5.0;

int target(unsigned char one, int two, unsigned int three, long four)
{
    /* force spill by creating lots of conflicting pseudos
     * validate that we spill the variable should_spill, which is used least
     * and has highest degree
     * Note: this isn't a good test of spill metric calculation;
     * due to optimistic coloring, we could end up spilling just should_spill
     * even if we end up choosing other nodes as spill candidates first
     */
    unsigned int five = -one;
    long six = glob2 * 2;
    char should_spill = glob + 3;
    // all these registers conflict with should_spill and each other
    unsigned long seven = one * one + 6ul;
    int *eight = &glob;
    signed char nine = two * 4;
    int ten = four + six;
    double *eleven = &glob3;
    unsigned int twelve = (unsigned int) -five;

    int result = callee(twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);

    // make another twelve pseudoes that conflict w/ should_spill and each other
    unsigned long int thirteen = glob + glob;
    double  *fourteen = &glob3;
    long fifteen = 12 - glob;
    int sixteen = thirteen * 3;
    int *seventeen = &glob2;
    int eighteen = fifteen + sixteen;
    unsigned int nineteen = glob2 * thirteen;
    unsigned char twenty = result * thirteen;
    int twenty_one = result + sixteen;
    unsigned int twenty_two = fifteen - result;
    int twenty_three = eighteen - nineteen;
    unsigned char twenty_four = twenty_one + twenty_two;
    long result2 = callee(thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, twenty_one, twenty_two, twenty_three, twenty_four);
    return should_spill + result2;
}
