/* Test linking against a double defined in another file */
extern double d;

int main() {
    return d == 1e20;
}