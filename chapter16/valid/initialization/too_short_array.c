int main()
{
    /* if some elments are explicitly initialized, remaining elements
     * should be initialized to zero
     */
    int arr[3] = {1};
    return arr[0];
}