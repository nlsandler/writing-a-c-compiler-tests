int main() {
    /* if a constant is too large to store as an int,
     * it's automatically converted to a long, even if it
     * doesn't have an 'l' suffix
     */
    return (17179869184 > 100l); // 17179869184 == 2^34
}