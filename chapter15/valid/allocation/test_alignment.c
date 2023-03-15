int main(void)
{
    int arr[5] = {0};
    int arr2[7] = {0};

    // make sure both arrays are 16-byte aligned and don't overlap
    unsigned long addr = (unsigned long)arr;
    if (addr % 16 != 0)
        return 0;

    for (int i = 0; i < 5; i = i + 1)
        arr[i] = i;

    addr = (unsigned long)arr2;
    if (addr % 16 != 0)
        return 0;

    // make sure we didn't overwrite arr2
    for (int i = 0; i < 7; i = i + 1)
        if (arr2[i])
            return 0;
    return 1;
}