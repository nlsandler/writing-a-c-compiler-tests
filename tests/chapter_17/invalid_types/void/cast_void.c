int main(void) {
    // you can't cast a void expression to another type
    int y = (int) (void) 3;
    return y;
}