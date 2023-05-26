int main(void)
{
    // can't initialize a static scalar object w/ a compound initializer
    // NOTE: this is undefined but technically not a constraint violation so maybe don't test it?
    static int x = {1, 2, 3};
    return x;
}