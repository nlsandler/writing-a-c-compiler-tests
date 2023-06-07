int x(int i) {
    return (i == 5);
}

int main(void) {
    return x(9223372036854775813ul);
}