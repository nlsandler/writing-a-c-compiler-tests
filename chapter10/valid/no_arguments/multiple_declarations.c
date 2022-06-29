int main() {
    int f();
    int f(void);
    return f();
}

int f(void) {
    return 3;
}