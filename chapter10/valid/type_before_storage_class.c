/* You can declare an identifier with the type specifier
 * before the storage class specifier.
 */

int static foo() {
    return 3;
}

int static bar = 4;

int main() {
    int extern foo();
    int extern bar;
    return foo() + bar;
}