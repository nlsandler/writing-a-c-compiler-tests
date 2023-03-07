int main() {
    int a = 0;
    switch(a) {
        case 1:
            switch(a) {
                case 0: return 0;
                default: return 0;
            }
        default: a = 2;
    }
    return a;
}