int main(void)
{
    // can't initialize a scalar expression w/ a compound initializer
    // NOTE: this is undefined but technically not a constraint violation so maybe don't test it?
    int x = {1, 2, 3};
    return x;
}