struct ten_bytes {
    char arr[10];
};

// irregularly-sized struct that's right on a page boundary
extern struct ten_bytes on_page_boundary;

struct ten_bytes return_struct(void) {
    on_page_boundary.arr[9] = -1;
    on_page_boundary.arr[8] = -2;
    on_page_boundary.arr[7] = -3;
    return on_page_boundary;
}

int main(void) {
    struct ten_bytes x = return_struct();
    for (int i = 0; i < 7; i = i + 1) {
        if (x.arr[i]) {
            return 1;
        }
    }

    if (x.arr[7] != -3) {
        return 2;
    }
    if (x.arr[8] != -2) {
        return 2;
    }
    if (x.arr[9] != -1) {
        return 3;
    }
    return 0;
}