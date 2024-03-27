int main(void)
{
    long x[3] = {0, -1, -2};
    long *y = x;
    // y++;
    ++y;
    return *y == -1;
}