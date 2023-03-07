int main()
{
    double arr[3] = {0, 1, 2};
    double *end_ptr = arr - (-2);
    return *end_ptr;
}