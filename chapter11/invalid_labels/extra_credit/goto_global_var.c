int x = 10;

int main() {
    /* goto statements can only target labels, not variables. */
    goto x;
    return 0;
}