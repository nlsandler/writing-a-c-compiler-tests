int main() {
    int a = 3;
    switch(a + 1) {
        case 0:
            a = 4;
            continue;
        default: a = 1;
    }
    return a;
}