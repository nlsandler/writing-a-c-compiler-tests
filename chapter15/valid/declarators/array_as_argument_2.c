// test that array types in parameters are converted to pointer types

int foo(int a[5])
{
    a[4] = 0;
    return 0;
}

int foo(int a[2]);

int main(void)
{
    int arr[8] = {8, 7, 6, 5, 4, 3, 2, 1};
    foo(arr);
    return arr[4];
}

int foo(int *a);