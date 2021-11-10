/* Test that we can explicitly convert a pointer to an integer type */
static long l;

int main() {
    long *ptr = &l;
    unsigned long ptr_as_long = (unsigned long) ptr;
    // long is eight-byte aligned, so the address of l
    // must be divisible by 8
    return (ptr_as_long % 8 == 0);
}