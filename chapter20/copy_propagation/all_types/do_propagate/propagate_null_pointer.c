int *return_ptr()
{
    int *ptr = 0;
    int *ptr2 = ptr;
    return ptr2;
}

int main()
{
    int *result = return_ptr();
    return (!result);
}