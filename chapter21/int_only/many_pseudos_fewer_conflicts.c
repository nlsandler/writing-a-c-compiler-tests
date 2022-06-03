int glob = 0;

int foo(int start, int end, int interval, int a, int b, int c)
{
    /* Test that we can assign non-conflicting pseudos
     * to the same register; there are more pseudoregisters than general-purpose registers,
     * BUT they don't all conflict, so we can allocate them without spills
     * Look for: no spills (requires optimizations to be enabled) */

    /* first, we'll calculate these */
    int d = start * 2;
    int e = 2;
    int f = 0;
    int g = 0;

    /* we'll declare these now, but they're dead */
    int h = 0;
    int i = 0;
    int j = 0;
    int k = 0;
    int l = 0;
    int m = 0;
    for (int counter = start; counter < end; counter = counter + interval)
    {
        d = d + a;
        e = e * b;
        f = f - glob;
        g = g - c;
    }

    if (!(d == 15 && e == 2048 && f == -10 && g == -25))
    {
        return 0;
    }

    /* from here out, a - g are dead. now we'll calculate h through m */
    h = start + 12;
    i = glob + h;
    j = glob - h;
    k = 2 + interval;
    l = 5;
    m = 6;
    while (h > 0)
    {
        i = i + j;
        j = j * 3;
        k = k - 4;
        l = l + 6;
        m = m + 8;
        h = h - 1;
    }

    if (h == 0 && i == -2657186 && j == -5314410 && k == -44 && l == 77 && m == 102)
        return 1;

    return 0;
}

int main()
{
    glob = 2;
    int result = foo(0, 10, 2, 3, 4, 5);
    return result;
}