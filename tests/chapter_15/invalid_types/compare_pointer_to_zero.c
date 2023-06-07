int main(void)
{
    int *x = 0;
    // illegal to compare a pointer w/ an intege
    // note that 0 isn't implicitly converted to a pointer here
    // it's only implicitly converted when used in == and != operations
    // Note: GCC/Clang only worry about this in -pedantic mode
    return x > 0;
}