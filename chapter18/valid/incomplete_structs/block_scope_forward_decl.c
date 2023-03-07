int main() {
    struct s;
    struct s *s_ptr = 0;
    struct s { int x; int y; };
    struct s val = { 1, 2 };
    s_ptr = &val;
    return s_ptr->x + s_ptr->y;
}