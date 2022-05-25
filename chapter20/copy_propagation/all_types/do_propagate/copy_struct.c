struct s
{
    int x;
    int y;
};

int main()
{
    static struct s s1 = {1, 2};
    struct s s2 = {3, 4};
    s1 = s2; // generate s1 = s2

    // make sure we're returning s2 (on stack) instead of s1 (on heap)

    return s1.x;
}