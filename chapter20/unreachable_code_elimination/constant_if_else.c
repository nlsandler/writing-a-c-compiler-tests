int main()
{
    // make sure jump/label/dead branch are optimized away, final add is not
    int x;
    if (0)
        x = 100;
    else
        x = 40;
    return x + 5;
}