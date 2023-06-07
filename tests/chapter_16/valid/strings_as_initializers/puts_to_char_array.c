// simple test of writing to char array
// and make sure puts works (test script validates stdout)

int puts(char *c);

int main(void)
{
    char str_array[2][6] = {"Hello", "World"};
    puts(str_array[0]);
    puts(str_array[1]);

    str_array[0][0] = 'J';
    puts(str_array[0]);

    return 0;
}