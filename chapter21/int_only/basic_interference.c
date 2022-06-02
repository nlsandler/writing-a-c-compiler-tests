int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;

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

/* this basically tests the same things as one_should_spill.c but maybe covers more ground wrt liveness analysis? */
int client()
{
    /* define some values - must be in calle-saved regs */
    int a = glob0;
    int b = glob1;
    int c = glob2;
    int d = glob3;
    int e = glob4;
    int f = glob5;
    reset_globals();
    glob0 = a;
    glob1 = b;
    glob2 = c;
    glob3 = d;
    glob4 = e;
    glob5 = f;
    return 0;
}

int main()
{
    client();
    return glob0 == 0 && glob1 == 1 && glob2 == 2 && glob3 == 3 && glob4 == 4 && glob5 == 5;
}