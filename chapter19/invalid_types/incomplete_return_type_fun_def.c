struct s return_struct() {
    struct s {
        int a;
        int b;
    };

    struct s result = { 1, 2 };
    return result;
}

int main() {
    return 0;
}