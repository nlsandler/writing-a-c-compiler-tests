/* It's illegal to initialize a static pointer with a non-pointer value */
static int *x = 10;

int main() {
    return 0;
}