int main() {
    int a = 2;
    switch (a) {
        case 2:
            a = 3;
            break;
        case 3:
            a = 4;
            break;
        default:
            a = 5;
            break;
    }
    return a;
}