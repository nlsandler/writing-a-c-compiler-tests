/* CopyToOffset does not kill src struct */

struct s {
    int a;
    int b;
    int c;
};

struct s glob = {1, 2, 3};

int main(void) {
    struct s my_struct = glob;  // not a dead store
    my_struct.c = 100;          // this doesn't make my_struct dead
    return (my_struct.c == 100 && my_struct.a == 1 && glob.c == 3);
}