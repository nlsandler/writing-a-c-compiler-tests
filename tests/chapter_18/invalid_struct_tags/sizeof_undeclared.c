int main(void) {
    // can't take the size of an undeclared struct type
    return sizeof(struct c);
}

struct c {
    int x;
};