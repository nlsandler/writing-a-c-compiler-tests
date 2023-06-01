struct s {
    char *str;
    int *x;
};

int main(void) {
    struct s my_struct = { "hello, world", 0};
    return my_struct.str[2] == 'l';
}