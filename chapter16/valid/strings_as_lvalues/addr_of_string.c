int main(void) {
    char (*string_literal)[12] = &"hello world";
    return string_literal[0][3];
}