/* If a static array isn't explicitly initialized, eveyr lement should be initialized to zero */
int arr[5][2][4];

int main(void)
{
    for (int i = 0; i < 5; i = i + 1)
        for (int j = 0; j < 2; j = j + 1)
            for (int k = 0; k < 4; k = k + 1)
                if (arr[i][j][k] != 0)
                    return 0;
    return 1;
}