struct s {
    char *str;
    int *x;
};

struct s my_struct = { "hello, world", 0};

int main() {
    return my_struct.str[2] == 'l';
}