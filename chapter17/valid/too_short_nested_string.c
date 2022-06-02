int puts(char *c);

int main()
{
    char str_array[2][10] = {"Hello", "World"};
    puts(str_array[0]);
    puts(str_array[1]);
    for (int i = 5; i < 10; i = i + 1)
        if (str_array[0][i] != 0 || str_array[1][i] != 0)
            return 1;

    return 0;
}