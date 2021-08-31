/* Test initializing and updating a long global variable */
static long foo = 4294967290l;

int main() {
    if (foo + 5l == 4294967295l) {
        return 1;
    }
    return 0;
}