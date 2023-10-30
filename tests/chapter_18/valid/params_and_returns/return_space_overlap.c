struct s {
    long l1;
    long l2;
    long l3;
};

extern struct s globvar;
struct s overlap_with_globvar(void);
struct s overlap_with_pointer(struct s *ptr);
int main(void) {
    globvar = overlap_with_globvar();
    if (globvar.l1 != 400l || globvar.l2 != 500l || globvar.l3 != 600l) {
        return 2;
    }

    struct s my_struct = {10l, 9l, 8l};
    my_struct = overlap_with_pointer(&my_struct);
    if (my_struct.l1 != 20l || my_struct.l2 != 18l || my_struct.l3 != 16l) {
        return 4;
    }
    return 0;
}