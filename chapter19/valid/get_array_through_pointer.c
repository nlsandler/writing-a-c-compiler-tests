void *malloc(unsigned long size);

struct struct_with_array {
    int x;
    double arr[3];
};

int main() {
    struct struct_with_array *s = malloc(sizeof(struct struct_with_array));
    double *d = s->arr;
    s->arr[2] = 4.5;
    return (d[2] == 4.5);
}