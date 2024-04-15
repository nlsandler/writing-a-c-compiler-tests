/* Make sure we use arithmetic rather than logical right shift */
int main(void) {
    return -5 >> 30;
}