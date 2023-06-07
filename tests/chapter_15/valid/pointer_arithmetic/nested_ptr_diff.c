int main(void)
{
    int multidim[6][7][4][2];
    int(*ptr1)[2] = multidim[3][4];
    int(*ptr2)[2] = &multidim[3][4][3];
    return ptr2 - ptr1;
}