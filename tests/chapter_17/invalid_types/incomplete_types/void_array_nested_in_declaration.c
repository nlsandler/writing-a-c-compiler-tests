extern void (*ptr)[3][4];  // array of void is illegal (including nested array)

void *foo(void) {
    return ptr;
}