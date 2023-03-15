/* Make sure that a callee can update an object through a variable passed by the caller */
int update_value(int *ptr) {
    int old_val = *ptr;
    *ptr = 10;
    return old_val;
}

int main(void) {
    int x = 20;
    int result = update_value(&x);
    return (x == 10 && result == 20);
}