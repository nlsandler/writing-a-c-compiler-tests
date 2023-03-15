/* first element should be 10.0, other three elements should be 0 */
double double_arr[2][2] = {{10.0}};

/* last element is 0 */
unsigned uint_arr[5] = {
    1u,
    1125899906842624l, // truncated to 0
    2147497230u,
};

unsigned long ulong_arr[4][6][2] = {
    {{
         1000.3,
     }, // truncated to 1000
     {12u}},
    {{2}}};

int main(void)
{
    double dbl_sum = double_arr[0][0] + double_arr[0][1] + double_arr[1][0] + double_arr[1][1];
    if (dbl_sum != 10.0)
        return 0;

    // check non-zero elements of uint_arr
    if (uint_arr[0] == 1 && uint_arr[2] == 2147497230u)
    {
        // check zero elements of uint_arr
        if (uint_arr[1] || uint_arr[3] || uint_arr[4])
        {
            return 0;
        }

        // now check ulong_arr
        for (int i = 0; i < 4; i = i + 1)
            for (int j = 0; j < 6; j = j + 1)
                for (int k = 0; k < 2; k = k + 1)
                {
                    int val = ulong_arr[i][j][k];
                    if (i == 0 && j == 0 && k == 0 && val != 1000u)
                        return 0;
                    if (i == 0 && j == 1 && k == 0 && val != 12)
                        return 0;
                    if (i == 1 && j == 0 && k == 0 && val != 2)
                        return 0;
                }

        return 1;
    }

    return 0;
}