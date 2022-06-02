void v() {
    ;
}

void x() {
    return v();
}

int main() {
    x();
    return 0;
}