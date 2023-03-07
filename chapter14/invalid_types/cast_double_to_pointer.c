/* It's illegal to cast a double to a pointer */

int main() {
    double d = 0.0;
    int *x = (int *) d;
    return 0;
}