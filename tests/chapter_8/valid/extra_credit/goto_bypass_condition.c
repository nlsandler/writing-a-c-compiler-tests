int main(void) {
    int i = 1;
    do {
        while_start:
        i = i + 1;
        if (i < 10)
            goto while_start;

    } while (0);
    return i;
}