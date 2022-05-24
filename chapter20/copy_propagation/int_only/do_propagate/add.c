int mult(int a, int b)
{
    return a * b;
}

int foo(int a, int b)
{
    int x = 10; // generate x = 10
    int y = 20; // generate y = 20
    x = a + b;  // kill x = 10
    // should become mult(x, 20)
    // look for movl $20, %esi
    // dst of addl should be source of movl to edi (or, should be rdi)
    // NOTE: mention that tests assume no function inlining...
    // or just have separate compilation unit to prevent that
    return mult(x, y);
}

int main()
{
    return foo(5, 6);
}