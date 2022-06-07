// NOTE: should also do an int-only version but it's easier w/ doubles b/c no XMM registers are callee-saved

double glob = 2.0;

double bar(double arg)
{
    return arg + 4.0;
}

double foo(double arg)
{
    // make sure both arg and result are coalesced into xmm0
    // conflcit graph: every XMM register conflicts w/ many_conflicts,
    // so both coalescings would fail the briggs test, but they pass the
    // george test b/c only neighbor of arg or result is many_conflicts,
    // which ALSO conflicts w/ xmm0
    double many_conflicts = glob;
    double result = bar(arg); // now many_conflicts conflicts w/ every XMM reg
    return result + many_conflicts;
}

int main()
{
    return foo(4.0);
}