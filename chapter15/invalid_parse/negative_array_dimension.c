/* could be type error
 * we don't accept this b/c we don't accept any constant expressions in array declarators,
 * only constant literals
 */
int main(void)
{
    int arr[-3];
    return 0;
}