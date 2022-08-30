/* first element should be 10.0, other threee elements should be 0 */
double double_arr[2][2] = {{10.0}};

int main()
{
    double sum = double_arr[0][0] + double_arr[0][1] + double_arr[1][0] + double_arr[1][1];
    return sum;
}