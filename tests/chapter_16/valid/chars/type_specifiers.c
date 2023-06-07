// make sure we can parse all ways to specify signed  &unsigned char

char signed static a = 10;
unsigned static char b = 20;

int main(void)
{
    extern signed char a;
    char unsigned extern b;
    return a + b;
}