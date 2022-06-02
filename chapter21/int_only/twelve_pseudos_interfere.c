int consume(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j, int k, int l)
{
    return a == 12 && b == 11 && c == 10 && d == 9 && e == 8 && f == 7 && g == 6 && h == 5 && i == 4 && j == 3 && k == 2 && l == 1;
}

int foo(int one, int two, int three, int four, int five, int six)
{
    /* all these arguments interfere so make sure we assign each one to a separate register
     * confirm: no spills, callee-saved regs are preserved
     */
    int seven = one + 6;
    int eight = two * 4;
    int nine = three * three;
    int ten = four + six;
    int eleven = 16 - five;
    int twelve = six + six;

    return consume(twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);
}

int main()
{
    return foo(1, 2, 3, 4, 5, 6);
}