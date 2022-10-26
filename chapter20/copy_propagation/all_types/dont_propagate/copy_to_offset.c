struct s
{
    int x;
    int y;
};

int main()
{
    static struct s s1 = {1, 2};
    struct s s2 = {3, 4};
    s1 = s2;  // generate s1 = s2
    s2.x = 3; // kill s1 = s2

    // how to recognize that we're accessing s1 and not s2?
    // it's annoying, but need to recognize that it originates in s1 (which is labeled...)

    return s1.x;
}