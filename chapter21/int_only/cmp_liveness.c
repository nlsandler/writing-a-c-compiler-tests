/* using a value in a comparison keeps it live, doesn't kill it
 * look for: no spills - exactly five callee-saved regs conflict at any time */

int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;

// use this to force pseudoregs to be callee-saved
int reset_globals()
{
    int old_glob0 = glob0;
    glob0 = 0;
    glob1 = 0;
    glob2 = 0;
    glob3 = 0;
    glob4 = 0;
    glob5 = 0;
    return old_glob0;
}

int use_value(int v)
{
    glob0 = glob0 + v;
    return 0;
}

int client(int flag)
{
    /* define some values - must be in calle-saved regs */
    int a = glob0;
    int b = glob1;
    int c = glob2;
    int d = glob3;
    int e = glob4;
    int f;
    int g;
    int h;
    int i;
    int j;
    // put this in conditional so copy prop doesn't get rid of these copies
    if (flag)
    {
        reset_globals();
        f = a; // now f interferes w/ b, c, d, and e but not a

        // use a but don't kill it - still no conflict w/ f
        if (a > 1)
        {
            glob0 = glob0 + 1;
        }
        g = b; // now g interferes w/ c, d, e, f but not a, b
        if (b < 10)
        {
            glob0 = glob0 + 2;
        }
        h = c; // h interferes with d, e, f, g, h but not a, b or c
        if (c <= 10)
            glob0 = glob0 + 3;

        i = d; // i interferes with e, f, g, h but not a, b, c, or d
        if (d >= 10)
            glob0 = glob0 + 4;
        j = e; // j interferes with f, g, h, i but not a, b, c,d, e
        if (e == 4)
            glob0 = glob0 + 5;
    }
    else
    {
        e = 0;
        f = 0;
        g = 0;
        h = 0;
    }
    int old_glob0 = reset_globals();
    if (f != 0)
        return 0;
    if (g != 1)
        return 0;
    if (h != 2)
        return 0;
    if (i != 3)
        return 0;
    if (j != 4)
        return 0;
    if (old_glob0 != 10)
        return 0;
    return 1;
}

int main()
{
    return client(1);
}