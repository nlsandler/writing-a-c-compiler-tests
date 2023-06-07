int main(void) {
    int x = 1;
    goto post_declaration;
    int i = (x = 0);
    post_declaration:
    i = 5;
    return (x == 1 && i == 5);
}