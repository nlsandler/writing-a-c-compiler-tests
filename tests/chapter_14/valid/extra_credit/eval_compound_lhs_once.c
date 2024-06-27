// Make sure we evaluate the lhs of a compound expression only once

int i = 0;

int putchar(int c);
int *print_A(void) {
    putchar(65); // write A to stdout
    return &i;
}

int main(void) {

    // we should print "A" to stdout only ONCE
    *print_A() += 5;
    if (i != 5) {
        return 1;
    }
    return 0; // success
}