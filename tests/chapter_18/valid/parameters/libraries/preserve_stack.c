struct my_struct {
    char arr[7];
};

static struct my_struct internal;

void process_struct(struct my_struct arg) {
    internal = arg;
}

int check_struct(void) {
    if (internal.arr[0] || internal.arr[1] || internal.arr[2]) {
        return 1;
    }
    if (internal.arr[3] != 1 || internal.arr[4] != 2 || internal.arr[5] != 3 ||
        internal.arr[6] != 4) {
        return 1;
    }
    return 0;
}