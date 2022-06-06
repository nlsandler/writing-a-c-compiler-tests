int consume(double a, double b, double c, double d, double e, double f, double g, double h, double i, double j, double k, double l, double m, double n)
{
    return a == 1 && b == 2 && c == 3 && d == 4 && e == 5 && f == 6 && g == 7 && h == 8 && i == 9 && j == 10 && k == 11 && l == 12 && m == 13 && n == 14;
}

int foo(double one, double two, double three, double four, double five, double six, double seven, double eight)
{
    /* all these arguments interfere so make sure we assign each one to a separate register
     * confirm: no spills, right answer
     */
    double nine = one + eight;
    double ten = two * five;
    double eleven = three + eight;
    double twelve = six + six;
    double thirteen = nine + four;
    double fourteen = seven + seven;

    return consume(one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen);
}

int main()
{
    return foo(1, 2, 3, 4, 5, 6, 7, 8);
}