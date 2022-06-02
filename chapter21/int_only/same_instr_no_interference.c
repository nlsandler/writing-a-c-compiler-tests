/* test that addl x, y does NOT create conflict b/t x and y if x is dead afterward
 * look for: no spills - there are eight callee-saved regs but they don't all conflict */

int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;

// use this to force pseudoregs to be callee-saved
int reset_globals()
{
    glob0 = 0;
    glob1 = 0;
    glob2 = 0;
    glob3 = 0;
    glob4 = 0;
    glob5 = 0;
    return 0;
}

int client()
{
    /* define some values - must be in calle-saved regs */
    int a = glob0;
    int b = glob1;
    int c = glob2;
    int d = glob3;
    reset_globals();
    int e = glob0 - a; // now e interferes w/ b, c, d but not a
    int f = glob1 - b; // now f interferes w/ d, c and e but not a or b
    int g = glob2 - c; // g interferes with d, e, f but not a, b, or c
    int h = glob3 - d; // h interferes with e, f, g but not a, b, c, d
    reset_globals();
    if (e != 0)
        return 0;
    if (f != -1)
        return 0;
    if (g != -2)
        return 0;
    if (h != -3)
        return 0;
    return 1;
}

int main()
{
    return client();
}