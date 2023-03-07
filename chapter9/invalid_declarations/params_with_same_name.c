/* It's illegal for multiple parameters to a function to have the same name */
int foo(int a, int a) {
    return a;
}

int main() {
    return foo(1, 2);
}