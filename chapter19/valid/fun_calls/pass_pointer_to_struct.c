struct pair {
    int elem1;
    int elem2;
};

void set_pair(struct pair *ptr) {
    ptr->elem1 = 100;
    ptr->elem2 = 12;
}

int main() {
    struct pair p = {0, 0};
    set_pair(&p);
    return p.elem1 + p.elem2;
}