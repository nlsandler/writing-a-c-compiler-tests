/* NOTE: we should do an int_only version of this too (that's more throrough than the current one)
 * but this is a lot easier to test w/ arrays/structs */

int glob0 = 0;
int glob1 = 1;
int glob2 = 2;
int glob3 = 3;

int populate(char *arr, int idx)
{
    if (idx < 0)
        return 0;
    arr[idx] = idx;
    return populate(arr, idx - 1);
}

int main()
{
    char arr[7];
    int w = glob0;
    int x = glob1;
    int y = glob2;
    int z = glob3;
    // make sure stack is sixteen-byte aligned for this call
    int result = populate(arr, 6);
    for (int i = 0; i < 7; i = i + 1)
        if (arr[i] != i)
            return 0;
    return (w == 0 && x == 1 && y == 2 && z == 3 && result == 0);
}