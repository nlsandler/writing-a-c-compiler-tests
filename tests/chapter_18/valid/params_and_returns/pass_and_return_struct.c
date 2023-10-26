struct pair {
    int x;
    char y;
};

struct pair add_to_x(struct pair p) {
    p.x = p.x + 5;
    return p;
}

int main(void) {
    struct pair arg = {1, 4};
    struct pair result = add_to_x(arg);
    return result.x + arg.x + result.y;
}