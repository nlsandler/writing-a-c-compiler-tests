int main() {
    int x = 10;
    int y = x;
    int *ptr = &y;
    y = 5;
    return *ptr;
}