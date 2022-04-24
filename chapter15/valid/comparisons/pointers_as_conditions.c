/* Test out using pointers in boolean expressions or as controlling conditions,
 * which implicitly compares them to zero
 */

int main() {
    long x;
    long *ptr = &x;
    long *null_ptr = 0;

    // note that pointers can appear in boolean expressions
    // with operands of any other type
    if (5.0 && null_ptr)
        return 0;

    int a = 0;
    if (!(ptr || (a = 10)))
        return 0;

    // make sure the || expression short-circuited
    if (a != 0)
        return 0;

    // apply ! to pointer
    if (!ptr)
        return 0;

    // use a pointer as the controlling condition in a loop
    int i = 0;
    while (ptr) {
        if (i > 10)
            ptr = 0;
        i = i + 1;
    }
    return i;

}