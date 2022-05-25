int use(int *p1, int *p2)
{
    return p1 == p2;
}

int main()
{
    int i = 0;
    int *ptr = &i;
    int *ptr2 = ptr; // generate copy ptr2 = ptr
    *ptr = 10;       // this does NOT kill copy

    // make sure we move same value into rdi and rsi, or copy one into the other
    return use(ptr, ptr2);
}