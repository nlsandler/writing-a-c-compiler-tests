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
    int a = glob4;
    int b = glob3;
    int c = glob2;
    int d = glob1;
    int e = glob0;
    reset_globals();
    int f = a - glob0; // now f interferes w/ b, c, d, e but not a
    int g = b - glob1; // now g interferes w/ d, c, e, f but not a or b
    int h = c - glob2; // h interferes with d, e, f, g but not a, b, or c
    int i = d - glob3; // i interferes with e, f, g, h but not a, b, c, d
    int j = e - glob4; // j interferes with f, g, h, i, but not a, b, c, d
    reset_globals();
    if (f != 4)
        return 0;
    if (g != 3)
        return 0;
    if (h != 2)
        return 0;
    if (i != 1)
        return 0;
    if (j != 0)
        return 0;
    return 1;
}

int main()
{
    return client();
}