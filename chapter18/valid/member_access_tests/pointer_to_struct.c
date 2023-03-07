void *malloc(unsigned long size);

struct pair {
    unsigned long first_tag;
    int second_tag;
};

int main() {
    struct pair *ptr = (struct pair *) malloc(sizeof(struct pair));
    ptr->second_tag = 3;
    ptr->first_tag = -1;
    return (ptr->first_tag - ptr->second_tag == 18446744073709551612ul);
}