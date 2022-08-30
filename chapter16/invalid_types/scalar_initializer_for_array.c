int main()
{
    // can't initialize array w/ non-compound initializer
    // NOTE: this is undefined but technically not a constraint violation so maybe don't test it?
    int arr[1] = 4;
    return arr[0];
}