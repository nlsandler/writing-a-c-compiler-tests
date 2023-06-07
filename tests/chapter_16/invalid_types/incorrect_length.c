int main(void)
{
    // incompatible pointer type: &"x" has type char (*)[2],
    // can't initilize a variable of type char (*)[10]
    char(*string_pointer)[10] = &"x";
    return 0;
}