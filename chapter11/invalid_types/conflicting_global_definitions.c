/* This declaration of foo is also a definition,
 * since it includes an initializer.
 */
int foo = 3;

int main() {
    return 0;
}

/* This declaration of foo is also a definition,
 * since it includes an initializer.
 * This is illegal, because foo was already declared.
 */
int foo = 4;