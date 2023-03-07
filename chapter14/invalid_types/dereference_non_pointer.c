/* It's illegal to dereference an expression with a non-pointer type */
int main() {
    unsigned long l = 100ul;
    return *l;
}