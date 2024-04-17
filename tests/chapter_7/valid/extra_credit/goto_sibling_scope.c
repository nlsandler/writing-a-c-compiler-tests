int main(void) {
    int sum = 0;
    if (1) {
        int a = 5;
        goto other_if;
        sum = 0;  // not executed
    first_if:
        sum = sum + a;  // sum = 11
    }
    if (0) {
    other_if:;
        int a = 6;
        sum = sum + a;  // sum = 6
        goto first_if;
        sum = 0;
    }
    return sum;
}