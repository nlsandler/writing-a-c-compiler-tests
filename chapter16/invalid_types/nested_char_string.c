// can only use a string literal to initialize
// a char array, not a char[3] array
char arr[3][3] = "hello";

int main(void)
{
    return arr[0][2];
}