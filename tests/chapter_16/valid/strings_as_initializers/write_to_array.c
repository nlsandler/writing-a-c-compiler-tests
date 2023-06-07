// basic test of writing to a char array

int main(void)
{
    char literal[4] = "abc";
    char b = literal[2];
    literal[2] = 'x';
    char x = literal[2];
    return (b == 'b' && x == 'x');
}