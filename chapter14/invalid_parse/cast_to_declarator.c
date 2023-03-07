int main()
{
    // can only cast to declarator types, not abstract declarators
    return (int **a)(10);
}