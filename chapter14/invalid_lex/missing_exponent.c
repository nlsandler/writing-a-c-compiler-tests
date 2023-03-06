int main()
{
    // "30." won't match our regex b/c it's followed by a letter
    // "30.e" is a preprocessing number but not a valid constant
    double foo = 30.e;
    return 4;
}