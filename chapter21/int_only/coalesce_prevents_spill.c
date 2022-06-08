int consume(int a, int b, int c, int d, int e, int f, int g, int h, int i, int j, int k, int l, int m)
{
    return a + b + c + d + e + f + g + h + i + j + k + l + m;
}

int flag = 0;

int foo(int one, int two, int three, int four, int five, int six)
{
    int thirteen = one;
    if (flag)
    {
        int to_coalesce = two + two;
        one = to_coalesce; // causes conflict b/t one and thirteen -
                           // conflict goes away if we coalesce one into to_coalesce
                           // and then we can coalesce it into thirteen
        thirteen = to_coalesce;
    }
    int seven = one + 6;
    int eight = two * 4;
    int nine = three * three;
    int ten = four + six;
    int eleven = 16 - five;
    int twelve = six + six;
    // how to avoid copy prop replacing thirteen and fourteen w/ twelve, without introducing conflict?
    // create an alternate path that doesn't go through that copy...but then it goes
    return consume(thirteen, twelve, eleven, ten, nine, eight, seven, six, five, four, three, two, one);
}

int main()
{
    int a = foo(1, 2, 3, 4, 5, 6);
    flag = !flag;
    int b = foo(8, 7, 6, 5, 4, 3);
    return a + b;
}