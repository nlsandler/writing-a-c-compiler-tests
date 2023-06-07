int main(void)
{
    int arr[5] = {1, 2, 3, 4, 5};
    int gt = &arr[3] > &arr[1];
    int ge = &arr[2] >= &arr[2];
    int lt = arr + 4 < arr;
    int le = arr + 1 <= arr + 2;
    return (gt == 1 && ge == 1 && lt == 0 && le == 1);
}