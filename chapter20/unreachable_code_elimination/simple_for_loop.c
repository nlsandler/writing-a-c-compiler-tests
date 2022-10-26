int main()
{
    int x = 0;
    // unreachable code elimination should remove continue label, have no other effect
    for (int i = 0; i < 3; i = i + 1)
        x = x + 1;

    return x;
}