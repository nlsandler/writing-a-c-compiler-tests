struct pair {
    double d;
    char *c_ptr;
};

void update_char(struct pair *p) {
    *p->c_ptr = 3;
}

int main() {
    char c = 5;
    struct pair p = { 4.6, &c };
    update_char(&p);
    return c;
}