int foo()
{
    return 1;
}

int main()
{

    // make sure there's nothing after ret statement/epilogue
    // (except possibly one more ret statement/epilogue)
    return 2;
    int x = foo();
    int y = x * 3;
    if (foo())
        y = y - 1;

    return 3000;
}