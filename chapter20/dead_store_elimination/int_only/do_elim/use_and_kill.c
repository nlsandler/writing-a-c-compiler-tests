int main()
{
    // we can eliminate both assignments to x
    // (look for: no movl $10, no addition, no inc...no function body basically)
    int x = 10;
    x = x + 1;
    return 0;
}