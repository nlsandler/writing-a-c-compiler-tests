int f(long l, double d) {
    return l == 2 && d == -6.0;
}

int main() {
    /* Implicitly convert function arguments to the correct type */
    return f(2.4, -6);
}