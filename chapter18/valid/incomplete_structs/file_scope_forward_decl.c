struct s;
struct s *get_struct(void);
void *malloc(unsigned long size);

struct s {
    int x;
    int y;
};

int main(void) {
    struct s *ptr = get_struct();
    return ptr->y;
}

struct s *get_struct(void) {
    struct s *result = malloc(sizeof(struct s));
    result->x = 1;
    result->y = 2;
    return result;
}