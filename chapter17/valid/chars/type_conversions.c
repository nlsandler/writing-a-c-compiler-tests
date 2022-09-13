int f(int i, long l, unsigned u, unsigned long ul, double d, unsigned char uc)
{
    return (i == -10 && l == -10 && u == 4294967286u && ul == 18446744073709551606ul && d == -10.0 && uc == 246);
}

signed char return_char()
{
    // implicit conversion from int to signed char
    return 4091;
}

int main()
{

    // signed char types to other types
    signed char sc = -10;
    // implicitly convert c to other types via parameter passing
    if (!f(sc, sc, sc, sc, sc, sc))
        return 1;
    char c = -10;
    if (!f(c, c, c, c, c, c))
        return 2;
    unsigned char uc = 250;
    int unsigned_convert = ((int)uc == 250 && (unsigned int)uc == 250 && (long)uc == 250 && (unsigned long)uc == 250 && (double)uc == 250.0 && (char)uc == -6 && (signed char)uc == -6);
    if (!unsigned_convert)
        return 3;

    // other types to signed char
    if ((sc = 128) != -128                      // int
        || (sc = 17592186044416l) != 0          // long
        || (sc = 2147483898u) != -6             // unsigned
        || (sc = 9224497936761618562ul) != -126 // unsigned long
        || (sc = uc) != -6                      // unsigned char
        || (sc = -2.6) != -2)                   // double
        return 4;

    sc = -1;
    // other types to unsigned char
    if ((uc = 252) != 252                      // int
        || (uc = 17592186044416l) != 0         // long
        || (uc = 2147483898u) != 250           // unsigned
        || (uc = 9224497936761618562ul) != 130 // unsigned long
        || (uc = sc) != 255                    // unsigned char
        || (uc = 35.9) != 35)                  // double
        return 5;

    // test cast from pointer to char (but not from char to pointer, result could be misaligned)
    long *null_ptr = 0;
    char zero = (char)null_ptr;

    if (zero)
        return 6;

    int retval = return_char();
    return (retval != -5);
}