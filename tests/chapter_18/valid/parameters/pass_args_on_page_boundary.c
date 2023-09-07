#ifdef SUPPRESS_WARNINGS
#pragma GCC diagnostic ignored "-Wunused-parameter"
#endif

struct nine_bytes {
    char arr[9];
};

// irregularly-sized struct that's right on a page boundary
extern struct nine_bytes on_page_boundary;


int f(struct nine_bytes in_reg, int a, int b, int c, int d, int e, struct nine_bytes stack1) {
    return in_reg.arr[2] + stack1.arr[3] + stack1.arr[8];
}

int main(void) {
    on_page_boundary.arr[2] = 4;
    on_page_boundary.arr[3] = 5;
    on_page_boundary.arr[8] = 6;
    // pass this struct in register and on stack
    return f(on_page_boundary, 0, 0, 0, 0, 0, on_page_boundary);
}