struct s;
struct s return_struct(void);

struct s {
    int a;
    int b;
};

int main(void) {
    struct s val = return_struct();
    return val.a;
}

struct s return_struct(void) {
    struct s result = { 1, 2 };
    return result;
}