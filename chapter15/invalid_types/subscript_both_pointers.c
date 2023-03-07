int main()
{
    int x = 10;
    int *ptr = &x;
    int *subscript = 0;
    // can't perform subscript operation when both operands are pointers
    return ptr[subscript];
}