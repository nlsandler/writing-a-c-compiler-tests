/* You can declare an identifier with the type specifier
 * before the storage class specifier.
 */

int static foo(void) {
    return 3;
}

int static bar = 4;

int main(void) {
    int extern foo(void);
    int extern bar;
    return foo() + bar;
}