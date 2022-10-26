int foo()
{
    return 10;
}

int bar()
{
    return 1 / 0;
}

int main()
{
    // when we enable unreachable code elimination and constant folding,
    // call to bar() should be optimized away, call to foo() shouldn't
    int i = 0;
    for (i = foo(); 0; i = i * 100)
        bar();
    return i;
}