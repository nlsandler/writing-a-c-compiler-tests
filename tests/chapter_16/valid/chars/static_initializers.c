// test statically initializing character types w/ other types of constants

char from_long = 17592186044416l;

char from_double = 15.6;

char from_uint = 2147483777u;

char from_ulong = 9223372037928517642ul;

signed char schar_from_long = 17592186044419l;

signed char schar_from_uint = 2147483898u;

signed char schar_from_ulong = 9223372037928517642ul;

signed char schar_from_double = 1e-10;

unsigned char uchar_from_int = 13526;

unsigned char uchar_from_uint = 2147483898u;

unsigned char uchar_from_long = 1101659111674l;

unsigned char uchar_from_ulong = 9223372037928517642ul;

unsigned char uchar_from_double = 77.7;

int main(void) {
  return (from_long == 0 && from_double == 15 && from_uint == -127 &&
          from_ulong == 10 && schar_from_uint == -6 && schar_from_ulong == 10 &&
          schar_from_double == 0 && uchar_from_int == 214 &&
          uchar_from_uint == 250 && uchar_from_ulong == 10 &&
          uchar_from_double == 77 && schar_from_long == 3 &&
          uchar_from_long == 250);
}