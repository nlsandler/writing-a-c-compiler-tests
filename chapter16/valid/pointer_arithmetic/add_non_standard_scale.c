int (*foo(int (*x)[7], long subscript))[7]
{
    return x + subscript;
}

int main()
{
    int my_array[3][7] = {{0}, {1, 2, 3, 4}};
    int(*second_array)[7] = foo(my_array, 1);
    return second_array[0][2];
}