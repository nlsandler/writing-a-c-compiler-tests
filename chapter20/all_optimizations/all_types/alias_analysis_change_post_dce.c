// if we perform alias analysis at the start of the loop, could we wind up in a situation where we miss optimizations
// that we'd catch by performing it right before copy prop

int main()
{
    int x = foo();
    if (x)
    {
        y = &x;
    }
}