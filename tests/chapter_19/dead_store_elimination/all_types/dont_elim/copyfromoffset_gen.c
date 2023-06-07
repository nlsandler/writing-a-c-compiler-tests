struct s
{
    int a;
    int b;
    int c;
};

int flag = 1;

int main(void)
{
    struct s s1 = {1, 2, 3};
    struct s s2 = {4, 5, 6};
    // can't
    struct s result = flag ? s1 : s2; // not a dead store b/c we access a member of result
    return result.c;
}