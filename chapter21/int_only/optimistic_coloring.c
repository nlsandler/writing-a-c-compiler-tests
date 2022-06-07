int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;
int glob4 = 4;
int glob5 = 5;
int flag = 0;

int increase_globals()
{
    glob0 = glob0 + 1;
    glob1 = glob1 + 1;
    glob2 = glob2 + 1;
    glob3 = glob3 + 1;
    glob4 = glob4 + 1;
    glob5 = glob5 + 1;
    return 0;
}

int getval()
{
    return 3;
}

int consume(int one, int two, int three, int four, int five)
{
    return one + two + three + four + five;
}
int foo()
{
    /* A - D are a clique; G - I are a clique;
     * E and F interfere with everything except each other
     */

    int e = getval();
    int f;
    if (flag)
    {
        int a = glob0;
        int b = glob1;
        int c = glob2;
        int d = glob3;
        increase_globals();
        // note: f wouldn't actually conflict w/ a-d if we had live range splitting
        consume(a, b, c, d, e);
        f = glob0;
        increase_globals();
        f = f + a + b + c + d;
    }
    else
    {
        int g = glob0;
        int h = glob1;
        int i = glob2;
        int j = glob3;
        increase_globals();
        consume(g, h, i, j, e);
        f = glob0;
        increase_globals();
        f = f + g + h + i + j;
    }
    int sum = getval();
    return sum + f;
}

int main()
{
    return foo() + foo();
}