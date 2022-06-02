struct s;
struct s get_struct();
void *malloc(unsigned long size);
struct s var;

struct s {
    int x;
    int y;
};

int main() {
    struct s val = get_struct();
    return val.y + var.y;
}

struct s var = { 4, 5 };

struct s get_struct() {
    struct s result;
    result.x = 1;
    result.y = 2;
    return result;
}