void f(int *arr)
{
    int *ptr = arr + 2;
    *ptr = 4; // this makes pointer live, so don't eliminate it!
    return;
}

int main()
{
    int arr[5] = {5, 5, 5, 5, 5};
    f(arr);
    return arr[2];
}