int main()
{
    // string literals can only initialize char arrays,
    // not arrays of other types
    long ints[4] = "abc";
    return ints[1];
}