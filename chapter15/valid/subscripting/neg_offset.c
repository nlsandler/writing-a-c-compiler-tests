int main()
{
    int foo[2][2] = {{1, 2}, {3, 4}};
    int(*foo_ptr)[2] = foo + 2;
    return foo_ptr[-1][0];
}