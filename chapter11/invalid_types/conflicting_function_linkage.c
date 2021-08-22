/* a function declared without the 'static'
 * keyword always has external linkage
 */
int foo();

int main() {
    return foo();
}

/* Can't define a symbol with external linkage,
 * then redefine it with internal linkage
 */
static int foo() {
    return 0;
}