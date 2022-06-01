int consume(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j, int k, int l)
{
    return a + b + c + d + e + f + g + h + i + j + k + l;
}

int foo(int one, int two, int three, int four, int five, int six)
{
    /* all these arguments interfere so make sure we assign each one to a separate register
     * confirm: no spills, callee-saved regs are preserved
     */
    int seven = one * 3;
    int eight = two - 5;
    int nine = three + 10;
    int ten = four * four;
    int eleven = -five;
    int twelve = six + seven;

    return consume(twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);
}

int main()
{
    return foo(10, 11, 12, 13, 14, 15);
}