int main() {
    unsigned long x = 100ul;
    unsigned long y = 18446744073709551605ul;
    return (y % x == 5ul);
}