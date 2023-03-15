// make sure we annotate string literals w/ correct type (accounting for length of null byte)

int main(void)
{
    // get one-past-the-end pointer to end of this string
    char(*str)[16] = &"Sample\tstring!\a" + 1;
    char *end_ptr = (char *)str - 1;
    // this should point to null byte
    return *end_ptr;
}