int main()
{
    int x = 0;
    // can't initialize pointer with value of type int
    // note that x isn't a null pointer onstant even though its value is 0
    int *ptr = x;
}