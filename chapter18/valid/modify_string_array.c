int printf(char *s);

int main() {
    char literal[15] = "hello, world!\n";
    literal[1] = 'u';
    printf(literal);
    return sizeof(literal);
}