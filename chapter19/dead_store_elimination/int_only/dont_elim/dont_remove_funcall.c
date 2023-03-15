int putchar(int c);

int main(void)
{
    // this is a dead store but we still shouldn't optimize away the function call!
    // remove store to x is safe but our implementation won't remove it
    int x = putchar(67);
    return 0;
}