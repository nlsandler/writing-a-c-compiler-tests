/* It's illegal to multiply, divide, or take the module of pointers */
int main(void) {
    int *x = 0;
    int *y = x;
    return (int) (x * y);
}