
int main()
{
    int arr[3][2][5] = {
        {{1, 2},
         {3, 4, 5}},
        {{6}},
        {{7},
         {8, 9, 10, 11, 12}}};

    int sum = arr[0][0][0] + arr[0][0][1] + arr[0][1][0] + arr[0][1][1] + arr[0][1][2] + arr[1][0][0] + arr[2][0][0];
    for (int i = 0; i < 5; i = i + 1)
        sum = sum + arr[2][1][i];

    return sum;
}