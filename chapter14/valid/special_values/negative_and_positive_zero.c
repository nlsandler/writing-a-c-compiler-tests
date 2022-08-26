int main()
{
    // make sure negative and positive zero are distinct constants
    double negative_zero = -0.0;
    double positive_zero = 0.0;

    if (negative_zero != positive_zero)
        return 0;

    // a positive number divided by negative zero is negative infinity
    if (1 / negative_zero != -10e308)
        return 0;

    // a positive number divided by zero is positive infinity
    if (1 / positive_zero != 10e308)
        return 0;

    return 1;
}