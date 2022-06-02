int glob = 0;

int foo(int start, int end, int interval, int a, int b, int c)
{
    /* force spill by creating lots of conflicting pseudos
     * validate that we get the right answer (of course) and
     * that we use every general-purpose register - even if we
     * have to spill, we should still allocate as many registers as possible
     * NOTE: just moving initial value from param reg into stack doesn't count
     * as using the reg */
    int d = start * 2;
    int e = 2;
    int f = 0;
    int g = 0;
    int h = 0;
    int i = 0;
    int j = 0;
    int k = 0;
    int l = glob;
    int m = 1;
    for (int counter = start; counter < end; counter = counter + interval)
    {
        d = d + 1;
        e = e * d;
        f = f - glob;
        g = g - 3;
        h = h + a;
        i = i + f;
        j = j + b;
        k = k + c;
        l = l + start;
        m = -2 * m;
    }

    if (d == 5 && e == 240 && f == -10 && g == -15 && h == 15 && i == -30 && j == 20 && k == 25 && l == 2 && m == -32)
    {
        return 0;
    }
    return 1;
}

int main()
{
    glob = 2;
    int result = foo(0, 10, 2, 3, 4, 5);
    return result;
}