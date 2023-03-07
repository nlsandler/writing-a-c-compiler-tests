/* make sure values of doubles are preserved across function calls (must be on the stack) */

double glob = 3.0;

double foo()
{
    return 4.0;
}

int main()
{
    double d = glob;
    double x = foo();
    return (d + x == 7.0);
}