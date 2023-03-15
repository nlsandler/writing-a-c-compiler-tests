int main(void)
{
    int arr[4] = {1, 2, 3, 4};
    int *ptr = arr + 3;
    return (arr - ptr == -3);
}