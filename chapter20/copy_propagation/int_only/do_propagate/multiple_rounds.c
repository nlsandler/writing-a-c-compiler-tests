int main()
{
    int x = 3;
    int y = x;
    return y; // look for movl $3, %eax (and two other movl $3, whatever too!)
}