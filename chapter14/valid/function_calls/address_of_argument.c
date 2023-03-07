/* Make sure we can take the address of function arguments,
 * not just variables */

int addr_of_arg(int a) {
    int *ptr = &a;
    *ptr = 10;
    return a;
}

int main() {
    // the parameter a is an lvalue with an address,
    // but the corresponding argument doesn't have to be
    int result = addr_of_arg(-20);
    return result; // result should be 10
}