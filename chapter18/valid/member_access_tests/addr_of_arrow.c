struct pair { int x ; int y; };

void *malloc(unsigned long size);

int main(void) {
    struct pair *s = malloc(sizeof(struct pair));
    s->x = 10;
    int *ptr = &(s->x);
    return *ptr;
}