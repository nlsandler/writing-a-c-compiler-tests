int main(void)
{
    // make sure we recognize chars as integer types and accept them in pointer arithmetic
    char *ptr = "foo";
    signed char null = ptr[3]; // terminating null byte, so value is 0
    if (ptr[null] != 'f')      // ptr[0] should be 'f'
        return 5;

    unsigned char index = 3;
    ptr = ptr + index; // points to null byte
    if (*ptr)
        return 6;
    char index2 = 2;
    return *(ptr - index2) == 'o';
}