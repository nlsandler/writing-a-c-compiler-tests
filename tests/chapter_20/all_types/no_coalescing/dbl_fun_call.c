/* make sure values of doubles are preserved across function calls (must be on the stack) */

double glob = 3.0;

double foo(void)
{
    return 4.0;
}

int main(void)
{
    double d = glob;
    double x = foo();
    return (d + x == 7.0);
}