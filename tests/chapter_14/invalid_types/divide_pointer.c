/* It's illegal to multiply, divide, or take the modulo of pointers */
int main(void)
{
    int x = 10;
    int *y = &x;
    return (y / 8);
}