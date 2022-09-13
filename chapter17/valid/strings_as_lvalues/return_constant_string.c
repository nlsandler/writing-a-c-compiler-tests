// test basic operations on pointers to constant strings - returning them, assigning them, pointer atihemtic, etc.

char *return_string()
{
    // constant strings have static storage duration,
    // so this will persist after the function call;
    return "I'm a string!";
}
int main()
{
    char *ptr = 0;
    ptr = return_string();
    if (!ptr)
        return 0;
    char *ptr2;
    ptr2 = 1 ? ptr + 2 : ptr + 4;
    return *ptr2 == 'm';
}