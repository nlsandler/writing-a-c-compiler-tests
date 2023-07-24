struct s {
    int a;
};

int main(void) {
    // you can't initialize a struct with a scalar expression, not even 0
    struct s x = 0;
    return x.a;
}