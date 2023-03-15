int main(void) {
    long l = 17179869184l; // 2**34
    // This long is implicitly converted to an int on assignment
    int i = l;
    return (i == 0);
}