int main()
{
    // note: my implementation failed this test
    // because I converted from the 64-bit Int64 type
    // to the 63 bit int type to perform negation!
    long l = -9223372036854775716l;
    unsigned long l2 = 9223372036854775900u;
    return l == l2;
}