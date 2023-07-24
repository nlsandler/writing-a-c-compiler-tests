int main(void) {
    struct s *ptr = 0;
    *ptr;  // can't dereference pointer to undeclared/incomplete struct
    return 0;
}