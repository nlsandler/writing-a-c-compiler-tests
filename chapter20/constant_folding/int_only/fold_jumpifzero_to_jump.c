int main()
{
    // look for: no conditional jumps, no cmp instruction
    int x = 0 && 0;
    return x;
}