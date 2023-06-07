struct inner {
    char a;
    char b;
};

struct middle {
    double d;
    struct inner i;
};

struct outer {
    struct middle m;
    long l;
};

struct outer global_struct;

void *malloc(unsigned long size);

int main(void) {
    struct outer *local_struct = (struct outer *) malloc(sizeof(struct outer));
    local_struct->l = 100;
    local_struct->m.d = 1.0;
    local_struct->m.i.a = 9;
    local_struct->m.i.b = 10;
    global_struct = *local_struct;
    return (global_struct.l == 100
            && global_struct.m.d == 1.0
            && global_struct.m.i.a == 9
            && global_struct.m.i.b == 10);
}