// test statically initializing character types w/ other types of constants

char from_long = 17592186044416l;

char from_double = 15.6;

signed char from_uint = 2147483898u;

unsigned char uchar_from_int = 13526;

unsigned char uchar_from_uint = 2147483898u;

int main()
{
    return from_long == 0 && from_double == 15 && from_uint == -6 && uchar_from_int == 214 && uchar_from_uint == 250;
}