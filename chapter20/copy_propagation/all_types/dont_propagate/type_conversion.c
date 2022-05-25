int main()
{
    int i = -1;
    unsigned int j = i;
    // don't replace signed w/ unsigned value here
    // NOTE: could handle this if we had separate signed/unsigned operators in TACKY
    return (j > 100);
}