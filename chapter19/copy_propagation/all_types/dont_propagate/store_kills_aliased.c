int flag(void)
{
    return 0;
}

int main(void)
{
    int i = 10;
    int j = 20;
    int *ptr1 = &i;
    int *ptr2 = &j;
    int *ptr = flag() ? ptr1 : ptr2;
    // kill i = 10 and j = 20
    *ptr = 100;
    return i + j;
}