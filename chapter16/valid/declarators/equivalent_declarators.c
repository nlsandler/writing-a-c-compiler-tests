/* Declare a global array multiple times w/ equivalent declarators */

long int(arr)[4] = {1, 2, 3, 4};

int long arr[4];

int (*ptr_to_arr)[3][6];

int((*(ptr_to_arr))[3l])[6u] = 0;

int main()
{
    return arr[2] == 3 && ptr_to_arr == 0;
}