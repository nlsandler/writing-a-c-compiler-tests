char c = 10;

int main()
{
    // this conflicts with previous definition of char,
    // because char and signed char are different types
    extern signed char c;
    return c;
}