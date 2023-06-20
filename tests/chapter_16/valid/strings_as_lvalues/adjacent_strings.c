/* Test that we concatenate adjacent string literal tokens */
int puts(char *s);

int main(void) {
    char *strings = "Hello," " World";
    puts(strings);
    return 0;
}