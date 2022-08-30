int main()
{
    int x = 10;
    int *y = &x + 1; // treat &x like one-element array - get pointer one past end of that array
    return *(y - 1);
}