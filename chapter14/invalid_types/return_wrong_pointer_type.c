/* It's illegal to return an int *
 * from a function with return type long *
 * because you can't implicitly convert
 * one pointer type to another
 */
int i;

long *return_long_pointer() {
    return &i;
}

int main() {
    long *l = return_long_pointer();
    return 0;
}