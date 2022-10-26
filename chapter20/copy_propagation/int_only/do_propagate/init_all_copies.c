// test that we initialize each basic block w/ incoming set of all copies
int stuff()
{
    return 1;
}
int something()
{
    static int i = 2;
    i = i - 1;
    return i;
}
int main()
{
    int y = 3;
    do
    {
        // when we first process this, one predecessor will having reaching copy y = 3
        // other predecessorw on't be processed yet
        stuff();
    } while (something());
    return y; // should become return 3
}