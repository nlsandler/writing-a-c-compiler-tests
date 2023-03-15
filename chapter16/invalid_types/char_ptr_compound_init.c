int main(void)
{
    // can't initialize a char * with a compound initializer
    char *ptr = {'a', 'b', 'c'};
    return 0;
}