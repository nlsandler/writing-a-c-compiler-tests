int main()
{
    long nested[4][5] = {{0}, {0}, {1, 2, 3}, {4, 5}};
    long(*ptr)[5] = nested + 4; // point one past end of array
    ptr = ptr - 2;              // point to second-to-lsat array element
    return (*ptr)[2];
}