int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;

int f()
{
    return 4;
}

int main()
{
    // make sure we adjust stack alignment correctly w/ an even number of callee-saved regs
    // when no other spills, no need to adjust
    // TODO figure out if this is redundant, may be covered by other tests?
    // look for: correct result
    int w = glob0;
    int x = glob1;
    int y = glob2;
    int z = glob3;
    int result = f();
    return (w == 0 && x == 1 && y == 2 && z == 3 && result == 4);
}