int main(void)
{
    int *x = 0;
    // can't subtract a pointer from an integer
    // Note that 0 is NOT implicitly converted to a pointer here
    return 0 - x == 0;
}