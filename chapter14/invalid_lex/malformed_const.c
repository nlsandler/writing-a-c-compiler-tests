int main()
{
    // this shouldn't match our floating-point regex b/c
    // "2."" is followed by a word character
    // in C standard terms, "2._" is a preprocessing number
    return 2._;
}