int client(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j, int k, int l)
{
    return a == 7 && b == 15 && c == 10 && d == 18 && e == 8 && f == 7 && g == 6 && h == 5 && i == 4 && j == 3 && k == 2 && l == 1;
}

int target(int one, int two, int three, int four, int five, int six)
{
    /* all these arguments interfere so make sure we assign each one to a separate register
     * validate that there are no spills aside from callee-saved regs at start and end
     * (there are also a few temporaries but they are also colorable once callee-saved regs are spilled)
     */

    int seven = one * one + 6;
    int eight = two * 4;
    int nine = three * two * three;
    int ten = four + six;
    int eleven = 16 - five + four;
    int twelve = six + six - five;

    return client(twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);
}