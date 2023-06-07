int main(void) {
    long x = 9223372036854775807l;
    return (!x); // test instruction rewrite rules for cmp $big_constant, $0
}