int a() {
    return 1;
}

int b(int a) {
    return a;
}

int main() {
    return a() + b(2);
}