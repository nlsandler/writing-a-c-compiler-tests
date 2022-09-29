struct s;
struct s return_struct();

struct s {
    int a;
    int b;
};

int main() {
    struct s val = return_struct();
    return val.a;
}

struct s return_struct() {
    struct s result = { 1, 2 };
    return result;
}