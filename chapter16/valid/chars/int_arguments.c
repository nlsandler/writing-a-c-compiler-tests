int foo(char a, char b, char c, unsigned char d, char e, char f) {
    return a + b + c + d + e + f;
}

int main(void) {
    int ret = foo(5, 300, 3, 255, -3, 8);
    return (ret == 312);
}