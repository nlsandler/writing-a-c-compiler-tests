/* addl x, y (or similar) causes interference if x is live afterwards */

/* test that addl x, y does NOT create conflict b/t x and y if x is dead afterward
 * look for: no spills - exactly five callee-saved regs conflict at any time
 * consider looking for movl %r15, %r15 etc -- or maybe that's too stringent
 * turn on optimizations to make sure we're testing the right thing */

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

int use_value(int v)
{
    glob0 = glob0 + v;
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
    int e = glob0 - a; // now e interferes w/ a, b, c, and d
    use_value(a);
    int f = glob1 - b; // now f interferes w/ b, d, c and e but not a
    use_value(b);
    int g = glob2 - c; // g interferes with c, d, e, f but not a or b
    use_value(c);
    int h = glob3 - d; // h interferes with d, e, f, g but not a, b, c
    use_value(d);
    if (e != 0)
        return 0;
    if (f != -1)
        return 0;
    if (g != -2)
        return 0;
    if (h != -3)
        return 0;
    if (glob0 != 6)
        return 0;
    return 1;
}

int main()
{
    return client();
}