/* if some elments are explicitly initialized, remaining elements
 * should be initialized to zero
 */
int arr[3] = {1, 2};

int main()
{
    return arr[0] + arr[1] + arr[2];
}