int main(void) {
    int sum = 0;
    for (int i = 0;; i = 0) {
    lbl:
        sum = sum + 1;
        i = i + 1;
        if (i > 10)
            break;
        goto lbl;
    }
    return sum;
}