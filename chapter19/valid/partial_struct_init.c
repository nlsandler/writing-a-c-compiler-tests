struct triple
{
    long one;
    double two;
    char three;
};

int main()
{
    struct triple array[3] = {{0},
                              {0, 9.0, 4},
                              {5, 6.0, 7}};
    struct triple new = {12, 11, 10};
    array[1] = new;
    return array[1].one + array[2].three + array[2].three + array[0].one;
}