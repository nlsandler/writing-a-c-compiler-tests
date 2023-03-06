int main()
{
    // this shouldn't match our floating-point
    // regex because "1." is followed by word character
    // (in C standard terms, 1.ex is a preprocessing number
    // that can't be converted into a constant token)
    return 1.ex;
}