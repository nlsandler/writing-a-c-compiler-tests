int foo(int a)
{
    return a;
    a = 10; // initialize ENTRY w/ empty set of copies, not including this one
}

int main(void)
{
    return foo(4);
}