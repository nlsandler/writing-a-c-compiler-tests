int main(void) {
    int i = 0;
    goto target;
    for (i = 5; i < 10; i = i + 1)
        target:
            if (i == 0)
                return 1;
    return 0;
}
