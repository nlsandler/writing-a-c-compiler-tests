int main(void)
{
    char z = 'z';
    char a = 'A';
    // these are both promoted so there's no overflow
    if (z + z + a != 309)
        return 1;

    unsigned char uc = 1;
    // because this is promoted to an int before negation,
    // the result is -1 instead of wrapping around to 255
    if ((int)-uc != -1)
        return 2;

    // b/c this is promoted to int before complement,
    // result is -2 instead of wrapping around to 254
    if ((int)~uc != -2)
        return 2;

    signed char w = 127;
    signed char x = 3;
    signed char y = 2;
    // we should promote all types to int so that intermediate result (127 + 3)
    // doesn't overflow; final result will fit in signed char
    signed char result = (w + x) / y;
    if (result != 65)
        return 3;

    // operating on signed/unsigned chars, both are converted to int
    signed char sc = -3;
    uc = 250;
    if (sc * uc != -750)
        return 4;

    char plain = -3;
    // common type of char and unsigned long is unsigned long
    if (plain * 1ul != 18446744073709551613ul)
        return 5;

    return 0;
}