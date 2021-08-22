/* A function parameter cannot have a storage class */
int f(extern int i) {
    return i;
}

int main() {
    return f(1);
}